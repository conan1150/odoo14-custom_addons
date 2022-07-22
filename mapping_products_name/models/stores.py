# -*- coding: utf-8 -*-
from odoo import models, fields, api


class store_list(models.Model):
    _name = 'store.list'
    _description = 'mapping_product_name.store_list'

    name = fields.Char('Store Name', required=True)
    store_group_id = fields.Many2one('store.group', string='Group Name')


class store_group(models.Model):
    _name = 'store.group'
    _description = 'mapping_product_name.store_group'

    name = fields.Char('Group Name')
    store_lists = fields.One2many('store.list', 'store_group_id', string='Store Lists')


