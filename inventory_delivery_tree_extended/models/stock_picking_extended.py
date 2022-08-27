# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'name desc'

    custom_ref = fields.Char("Customer Ref.", compute='_compute_order_ref', store=True)


    @api.depends('group_id')
    def _compute_order_ref(self):
        for ori in self:
            cus_ref = self.env['sale.order'].search([('name', '=', ori.group_id.name)])
            ori.custom_ref = cus_ref.client_order_ref
           