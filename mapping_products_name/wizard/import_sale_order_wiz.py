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
        data = pd.read_excel(BytesIO(base64.b64decode(self.file_data)), usecols=['product_name', 'variant', 'unit_price', 'product_qty'])

        order_data = []
        failed_data = []

        for order in data.to_dict(orient='records'):
            o_line = self._order_line(order['product_name'],
                                    "" if pd.isna(order['variant']) else order['variant'],
                                    order['product_qty'],
                                    order['unit_price'])

            if o_line['failed'] and o_line['product_name'] not in failed_data:
                failed_data.append(o_line['product_name'])
            else:
                order_data.append(o_line)            

        if failed_data is Empty:
            return order_data
        else:
            item_list = "\n".join(failed_data)
            raise UserError(_(f"Failed to import items. Please check the {len(failed_data)} items : \n\n {item_list}"))


    def _order_line(self, product_name, variant_name, product_qty, unit_price):
        product_id = self.env['store.products'].search([('name', '=', product_name), ('store_id', '=', self.store_id.id)])
        product_var = self.env['store.products.variant'].search([('name', '=', variant_name), ('store_product_id', '=', product_id.id)])

        p_id = self.env['map.product.to.other.stores'].search([('store_product_v_id', '=', product_var.id), ('store_id', '=', self.store_id.id)]).product_id.id

        if p_id:
            data_line = {'product_code': product_id.store_product_default_code,
                        'product_name': product_name,
                        'variant_code': product_var.store_product_sub_code,
                        'product_qty': product_qty,
                        'unit_price': unit_price,
                        'product_id': p_id,
                        'failed': False}

            return data_line
        else:
            return {'product_name': product_name if product_var.name == "" else f'{product_name} [{product_var.name}]',
                    'failed': True}


    def sale_order_list_up(self):
        active_id = self.env.context.get('active_id')
        ex_data = self._read_file()

        for order_line in ex_data:
            self.env['sale.order.line'].create({'order_id': active_id,
                                                'product_id': order_line['product_id'],
                                                'product_uom_qty': order_line['product_qty'],
                                                'price_unit': order_line['unit_price']})
            self.env.cr.commit()

        return True




    
                


    
