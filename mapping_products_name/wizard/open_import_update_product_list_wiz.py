from odoo import api, models, fields
from odoo.exceptions import UserError

import os
import base64
from io import BytesIO
import pandas


class OpenImportUpdateProductListWiz(models.TransientModel):
    _name = 'open.import.update.product.list.wiz'

    store_id = fields.Many2one('store.list', string='Store', required=True)
    file_data = fields.Binary('File', required=True,)
    file_name = fields.Char('File Name')


    def _read_file(self):        

        master_data = pandas.read_excel(BytesIO(base64.b64decode(self.file_data)), usecols=['et_title_product_id',
                                                                                            'et_title_product_name',
                                                                                            'et_title_variation_id',
                                                                                            'et_title_variation_name',
                                                                                            'et_title_variation_price'])

        data_list = []

        for data in master_data.to_dict(orient='records'):
            master_data_db = self.env['store.products.variant'].search([('store_product_id.store_product_default_code', '=', data['et_title_product_id']),
                                                                        ('store_product_sub_code', '=', data['et_title_variation_id']),
                                                                        ('store_product_id.store_id', '=', self.store_id.id)])

            if master_data_db.id:
                if master_data_db.store_product_id.name != data['et_title_product_name']:
                    product_name = self.env['store.products'].browse(master_data_db.store_product_id.id)
                    product_name.write({'name': data['et_title_product_name']})

                
                if master_data_db.name != data['et_title_product_name']:
                    variation_name = self.env['store.products.variant'].browse(master_data_db.id)
                    variation_name.write({'name': data['et_title_product_name']})
            else:
                data_list.append()

        #     row_value = []
        #     c = 0
        #     for cell in row:
        #         row_value.append(int(cell.value) if c == 4 else cell.value)
        #         c += 1
        #     data.append(row_value)

        return data_list


    def update_product_list(self):
        data = self._read_file()
        # products = [p.store_product_default_code for p in self.env['store.products'].search([('store_id', '=', self.store_id.id)])]

        # for i in data:
        #     if i[0] not in products:        
        #         self.env['store.products'].create({'name': i[1],
        #                                             'store_id': self.store_id.id,
        #                                             'store_product_default_code': i[0],
        #                                             'price_by_store': i[4]})
        #         self.env.cr.commit()

        #         self.env['store.products.variant'].create({'name': i[3],
        #                                             'store_product_id': self.env['store.products'].search([('store_product_default_code', '=', i[0])]).id,
        #                                             'store_product_sub_code': i[2]})
        #         self.env.cr.commit()

        #         products += [i[0]]            
        #     else:
        #         main_code = self.env['store.products'].search([('store_product_default_code', '=', i[0])])
        #         var_code = self.env['store.products.variant'].search([('store_product_id', '=', main_code.id)])

        #         if i[2] not in [v.store_product_sub_code for v in var_code]:
        #             self.env['store.products.variant'].create({'name': i[3],
        #                                             'store_product_id': main_code.id,
        #                                             'store_product_sub_code': i[2]})                                                   
        #             self.env.cr.commit()

        return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
                


    
