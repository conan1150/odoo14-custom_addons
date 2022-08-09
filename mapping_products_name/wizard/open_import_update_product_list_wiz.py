from typing import Tuple
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
        master_data = pandas.read_excel(BytesIO(base64.b64decode(self.file_data)), skiprows=[1, 2, 3], usecols=['et_title_product_id',
                                                                                                                    'et_title_product_name',
                                                                                                                    'et_title_variation_id',
                                                                                                                    'et_title_variation_name',
                                                                                                                    'et_title_variation_price'])

        return master_data.to_dict(orient='records')


    def _check_existing_items_and_update_lists(self):
        for data_item in self._read_file():
            data = self.env['store.products.variant'].search([('store_product_id.store_product_default_code', '=', data_item['et_title_product_id']),
                                                                        ('store_product_sub_code', '=', data_item['et_title_variation_id']),
                                                                        ('store_product_id.store_id', '=', self.store_id.id)])

            if data.id:
                self._update_item_name_or_variation(data_item, data.id)                
            else:
                self._add_new_item(data_item)

        return True


    def _add_new_item(self, data_item):
        product_id = self.env['store.products'].search([('store_id', '=', self.store_id.id),
                                                        ('store_product_default_code', '=', data_item['et_title_product_id'])])

        if product_id.id:
            self._add_new_item_variation(data_item, product_id.id)
        else:
            self.env['store.products'].create({'name': data_item['et_title_product_name'],
                                                'store_id': self.store_id.id,
                                                'store_product_default_code': data_item['et_title_product_id'],
                                                'price_by_store': data_item['et_title_variation_price']})
            self.env.cr.commit()

            self._add_new_item_variation(data_item, self.env['store.products'].search([('store_product_default_code', '=', data_item['et_title_product_id'])]).id)

        return True


    def _add_new_item_variation(self, data_var_item, item_id):
        self.env['store.products.variant'].create({'name': "" if pandas.isna(data_var_item['et_title_variation_name']) else data_var_item['et_title_variation_name'],
                                                'store_product_id': item_id,
                                                'store_product_sub_code': data_var_item['et_title_variation_id']})
        self.env.cr.commit()

        return True


    def _update_item_name_or_variation(self, data_item, product_id):
        product_var_id = self.env['store.products.variant'].browse(product_id)

        if product_var_id.store_product_id.name != data_item['et_title_product_name']:
            product_name = self.env['store.products'].browse(product_var_id.store_product_id.id)
            product_name.write({'name': data_item['et_title_product_name'],
                                'price_by_store': float(data_item['et_title_variation_price'])})
            self.env.cr.commit()

        product_var_name = "" if pandas.isna(data_item['et_title_variation_name']) else data_item['et_title_variation_name']
        
        if product_var_id.name != product_var_name:
            product_var_id.write({'name': product_var_name})
            self.env.cr.commit()

        return True


    def update_data_click(self):
        self._check_existing_items_and_update_lists()

        return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

