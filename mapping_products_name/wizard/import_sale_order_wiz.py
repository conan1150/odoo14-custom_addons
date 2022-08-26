from queue import Empty
from odoo import api, models, fields, _
from odoo.exceptions import UserError

import os
import base64
from io import BytesIO
import pandas as pd

item_not_found = 0


class ImportSaleOrderWiz(models.TransientModel):
    _name = 'import.sale.order.wiz'

    store_id = fields.Many2one('store.list', string='Store', required=True)
    file_data = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')

    
    def _read_file(self):
        file_upload = self.env['import.file.data'].search([('name', '=', self.file_name)])
        
        try:
            if file_upload.id:
                raise ValueError(f"Please check this file '{self.file_name}' has been uploaded.")                
            else:
                file = self.env['import.file.data'].create({'name': self.file_name})
                self.env.cr.commit()

                data_file = pd.read_excel(BytesIO(base64.b64decode(self.file_data)), usecols=[0, 3, 4, 16, 18, 20, 21, 42, 43, 45, 46, 47, 48, 49])
                data_dict = [{'order_no': row[0],
                                'date_order': row[2],
                                'user_acc': row[1],
                                'parent_id': self.store_id.store_group_id.id,
                                'product_name': row[3],
                                'variant': "" if pd.isna(row[4]) else row[4],
                                'unit_price': row[5],
                                'qty': row[6],
                                'recipient_name': row[7],
                                'addr': {'phone_number': row[8].strip("*"),
                                        'address': row[9].split()[:-3],
                                        'country_id': row[10],
                                        'state_id': row[11].replace("จังหวัด", "").replace("มหานคร", ""),
                                        'city': row[12],
                                        'zip_code': str(row[13])
                                        },
                                } for index, row in data_file.iterrows()]

                for data in data_dict:
                    partner_id = self._contact_check(data['user_acc'], data['recipient_name'], data['addr'], data['parent_id'])

                    order_line = {                
                        'product_name': data['product_name'],
                        'variant': data['variant'],
                        'unit_price': data['unit_price'],
                        'qty': data['qty'],                        
                    }

                    if partner_id:
                        order_id = self.env['sale.order'].search([('client_order_ref', '=', data['order_no'])])

                        if order_id:
                            self._create_new_order_line(order_id.id, order_line)
                        else:
                            order_id_s = self._create_new_order(data['order_no'], data['date_order'], partner_id, file.id)
                            self._create_new_order_line(order_id_s, order_line)

        except ValueError as err:
            raise UserError(_(err))


    def _contact_check(self, contact_name, delivery_name, addr, parent_id):
        contact_id = self.env['res.partner'].search([('name', '=', contact_name), ('parent_id', '=', parent_id)])
        contact_addr = self._contact_address(addr)

        if contact_id:
            delivery_id = self.env['res.partner'].search([('name', '=', delivery_name), ('parent_id', '=', contact_id.id)])
            if delivery_id:
                return delivery_id.id
            else:
                self._add_new_contact(delivery_name, contact_id.id, contact_addr)
                return self.env['res.partner'].search([('name', '=', delivery_name), ('parent_id', '=', contact_id.id)]).id
        else:
            contact_id_s = self._add_new_contact(contact_name, parent_id)
            self._add_new_contact(delivery_name, contact_id_s.id, contact_addr)

            return self.env['res.partner'].search([('name', '=', delivery_name), ('parent_id', '=', contact_id_s.id)]).id           


    def _add_new_contact(self, contact_name, parent_id, address=None):
        if address == None:
            contact_id = self.env['res.partner'].create({'name': contact_name,
                                            'parent_id': parent_id,
                                            'type': 'contact',
                                            'is_company': False,
                                            'customer_rank': 1,
                                            'partner_gid': 0})
            self.env.cr.commit()
            return contact_id
        else:
            contact_id = self.env['res.partner'].create({'name': contact_name,
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
            return contact_id


    def _contact_address(self, addr):
        addr_position_cut = int(len(addr['address'])/2)

        addr1 = " ".join(addr['address'][:addr_position_cut + 1])
        addr2 = " ".join(addr['address'][addr_position_cut + 1:])
        
        addr['addr1'] = addr1
        addr['addr2'] = addr2
        addr.pop('address')
        
        state_area = self.env['res.country.state'].search([('name', '=', addr['state_id'])])
        addr['state_id'] = state_area.id
        addr['country_id'] = state_area.country_id.id

        return addr

    def _create_new_order(self, order_no, date_order, partner_id, file_id):        

        order_id = self.env['sale.order'].create({'client_order_ref': order_no,
                                        'date_order': date_order,
                                        'state': 'draft',
                                        'partner_id': partner_id,
                                        'store_id': self.store_id.id,
                                        'uploat_file_id': file_id})
        self.env.cr.commit()

        return order_id.id


    def _create_new_order_line(self, order_id, order_line):
        product_id = self.env['store.products'].search([('name', '=', order_line['product_name']), ('store_id', '=', self.store_id.id)])                

        if product_id.id:
            product_var = self.env['store.products.variant'].search([('name', '=', order_line['variant']), ('store_product_id', '=', product_id[-1].id)])
            if product_var.id:
                o_product_id = self.env['map.product.to.other.stores'].search([('store_product_v_id', '=', product_var.id), ('store_id', '=', self.store_id.id)]).product_id
            else:
                o_product_id = False
                order_line['state'] = 'product_v_error'
        else:
            o_product_id = False
            order_line['state'] = 'product_error'
        

        if o_product_id:
            self.env['sale.order.line'].create({'order_id': order_id,                                                
                                                'product_id': o_product_id[0].id,
                                                'product_uom_qty': order_line['qty'],
                                                'price_unit': order_line['unit_price']})
            self.env.cr.commit()
        else:
            global item_not_found
            item_not_found += 1

            order_line['order_no'] = self.env['sale.order'].browse(order_id).client_order_ref
            order_line['state'] = 'mapping_error'
            
            self.env['wrong.upload.so.list'].create({'name': order_line['order_no'],
                                                    'store_id': self.store_id.id,
                                                    'order_id': order_id,
                                                    'product_name': order_line['product_name'],
                                                    'product_variant': order_line['variant'],
                                                    'order_qty': order_line['qty'],
                                                    'unit_price': order_line['unit_price'],
                                                    'state': order_line['state']})
            self.env.cr.commit()
            # order_no.unlink()


    def sale_order_list_up(self):
        ex_data = self._read_file() 

        return {
            'name': _('Items not found!'),
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'warning',
                'title': _('Items not found!'),
                'message': f'{item_not_found} items not found.',
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
            },
        }
    
