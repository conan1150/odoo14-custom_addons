# -*- coding: utf-8 -*-
from odoo import models, fields, api


class store_list(models.Model):
    _name = 'store.list'
    _description = 'mapping_product_name.store_list'

    name = fields.Char('Store Name', required=True)
    store_group_id = fields.Many2one('res.partner', string='Group')
    

class Partner(models.Model):
    _inherit = 'res.partner'

    store_ids = fields.One2many('store.list', 'store_group_id', string='Store')
    