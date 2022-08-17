from queue import Empty
from odoo import api, models, fields, _
from odoo.exceptions import UserError

import os
import base64
from io import BytesIO
import pandas as pd


class ImportSaleOrderWiz(models.TransientModel):
    _name = 'import.sale.order.wiz'

    store_id = fields.Many2one('store.list', string='Store', required=True)
    file_data = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')


    def _read_file(self):        
        data_file = pd.read_excel(BytesIO(base64.b64decode(self.file_data)), usecols=[0, 3, 16, 18, 20, 21, 42, 43, 45, 46, 47, 48, 49])
        data_dict = [{'order_no': row[0],
                        'user_acc': row[1],
                        'parent_id': self.store_id.store_group_id.id,
                        'product_name': row[2],
                        'variant': "" if pd.isna(row[3]) else row[3],
                        'unit_prict': row[4],
                        'qty': row[5],
                        'recipient_name': row[6],
                        'addr': {'phone_number': row[7].strip("*"),
                                'address': row[8].split()[:-3],
                                'country_id': row[9],
                                'state_id': row[10].replace("จังหวัด", "").replace("มหานคร", ""),
                                'city': row[11],
                                'zip_code': str(row[12])
                                },
                        } for index, row in data_file.iterrows()]


        for data in data_dict:
            partner_id = self._contact_check(data['user_acc'], data['recipient_name'], data['addr'], data['parent_id'])

            order_line = {
                'product_name': data['product_name'],
                'variant': data['variant'],
                'unit_prict': data['unit_prict'],
                'qty': data['qty'],
            }

            if partner_id:
                order_id = self.env['sale.order'].search([('client_order_ref', '=', data['order_no'])])

                if order_id:
                    self._create_new_order_line(order_id.id, order_line)
                else:
                    order_id_s = self._create_new_order(data['order_no'], partner_id)
                    self._create_new_order_line(order_id_s, order_line)


    def _contact_check(self, contact_name, delivery_name, addr, parent_id):
        contact_id = self.env['res.partner'].search([('name', '=', contact_name), ('parent_id', '=', parent_id)])

        if contact_id:
            delivery_id = self.env['res.partner'].search([('name', '=', delivery_name), ('parent_id', '=', contact_id.id)])
            if delivery_id:
                return delivery_id.id
            else:
                addr_position_cut = int(len(addr['address'])/2)
                addr1 = " ".join(addr['address'][:addr_position_cut + 1])
                addr2 = " ".join(addr['address'][addr_position_cut + 1:])

                addr.pop('address')
                addr['addr1'] = addr1
                addr['addr2'] = addr2
                
                state_area = self.env['res.country.state'].search([('name', '=', addr['state_id'])])
                addr['state_id'] = state_area.id
                addr['country_id'] = state_area.country_id.id

                self._add_new_contact(delivery_name, contact_id.id, addr)
                return self.env['res.partner'].search([('name', '=', delivery_name), ('parent_id', '=', contact_id.id)]).id
        else:
            self._add_new_contact(contact_name, parent_id)
            contact_id = self.env['res.partner'].search([('name', '=', contact_name), ('parent_id', '=', parent_id)])
            if contact_id:
                self._add_new_contact(delivery_name, contact_id.id, addr)
                return self.env['res.partner'].search([('name', '=', delivery_name), ('parent_id', '=', contact_id.id)])


    def _add_new_contact(self, contact_name, parent_id, address=None):
        if address == None:
            self.env['res.partner'].create({'name': contact_name,
                                            'parent_id': parent_id,
                                            'type': 'contact',
                                            'is_company': False,
                                            'customer_rank': 1,
                                            'partner_gid': 0})
            self.env.cr.commit()
        else:
            self.env['res.partner'].create({'name': contact_name,
                                            'parent_id': parent_id,
                                            'type': 'delivery',
                                            'is_company': False,
                                            'customer_rank': 1,
                                            'street': address['addr1'],
                                            'street2': address['addr2'],
                                            'zip': address['zip_code'],
                                            'city': address['city'],
                                            'state_id': address['state_id'],
                                            'country_id': address['country_id'],
                                            'phone': address['phone_number']
                                            })
            self.env.cr.commit()


    def _create_new_order(self, order_no, partner_id):
        order_id = self.env['sale.order'].create({'client_order_ref': order_no,
                                        'state': 'draft',
                                        'partner_id': partner_id})
        self.env.cr.commit()
        return order_id.id


    def _create_new_order_line(self, order_id, order_line):
        product_id = self.env['store.products'].search([('name', '=', order_line['product_name']), ('store_id', '=', self.store_id.id)])
        product_var = self.env['store.products.variant'].search([('name', '=', order_line['variant']), ('store_product_id', '=', product_id.id)])

        print(product_var)

        # p_id = self.env['map.product.to.other.stores'].search([('store_product_v_id', '=', product_var.id), ('store_id', '=', self.store_id.id)]).product_id.id

        # if p_id:
        #     data_line = {'product_code': product_id.store_product_default_code,
        #                 'product_name': product_name,
        #                 'variant_code': product_var.store_product_sub_code,
        #                 'product_qty': product_qty,
        #                 'unit_price': unit_price,
        #                 'product_id': p_id,
        #                 'failed': False}

        #     return data_line
        # else:
        #     return {'product_name': product_name if product_var.name == "" else f'{product_name} [{product_var.name}]',
        #             'failed': True}


    def sale_order_list_up(self):
        ex_data = self._read_file()

        # for order_line in ex_data:
        #     self.env['sale.order.line'].create({'order_id': active_id,
        #                                         'product_id': order_line['product_id'],
        #                                         'product_uom_qty': order_line['product_qty'],
        #                                         'price_unit': order_line['unit_price']})
        #     self.env.cr.commit()

        return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }




    
                


    
