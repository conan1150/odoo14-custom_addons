from odoo import api, models, fields
from odoo.exceptions import UserError

import os
import base64
from io import BytesIO
import openpyxl


class ImportSaleOrderWiz(models.TransientModel):
    _name = 'import.sale.order.wiz'

    store_id = fields.Many2one('store.list', string='Store', required=True)
    file_data = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')


    def _read_file(self):        

        wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file_data)), data_only=True)
        ws = wb.active

        data = []

        worksheet = ws.iter_rows(min_row=2, min_col=17, max_row=None, max_col=None)

        for row in worksheet:
            row_value = {}

            p_code = self.env['store.products'].search([('name', '=', row[0].value), ('store_id', '=', self.store_id.id)])

            row_value['product_code'] = p_code.store_product_default_code
            row_value['product_name'] = row[0].value

            pvar_code = self.env['store.products.variant'].search([('name', '=', row[2].value), ('store_product_id', '=', p_code.id)])

            row_value['product_var_code'] = pvar_code.store_product_sub_code
            row_value['product_variant'] = row[2].value

            row_value['product_qty'] = row[5].value
            row_value['product_price'] = float(row[4].value)
            
            data.append(row_value)

        return data


    def sale_order_list_up(salf):
        data = salf._read_file()
        active_id = salf.env.context.get('active_id')
                
        
        for d in data:
            p_by_store_id = salf.env['store.products.variant'].search([('store_product_id.store_product_default_code', '=', d['product_code']), ('store_product_sub_code', '=', d['product_var_code'])]).id
            d['product_tmpl_id'] = salf.env['map.product.to.other.stores'].browse(p_by_store_id).id

            print(d)

    
                


    
