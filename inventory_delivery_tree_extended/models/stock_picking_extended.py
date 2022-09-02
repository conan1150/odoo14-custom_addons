# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'name desc'

    custom_ref = fields.Char("Custom Ref.", compute='_compute_order_ref', store=True)
    # custom_no = fields.Many2one(related="group_id.sale_id.client_order_ref", string="Sales Order", store=True, readonly=False)


    @api.depends('group_id', 'origin')
    def _compute_order_ref(self):
        for ori in self:
            # cus_ref = self.env['sale.order'].search([('name', '=', ori.group_id.name)])
            # ori.custom_ref = cus_ref.client_order_ref

            print(ori.picking_type_id)
            if ori.picking_type_id.id == 2:
                cus_ref = self.env['sale.order'].search([('name', '=', ori.group_id.name)])
                ori.custom_ref = cus_ref.client_order_ref
            elif ori.picking_type_id.id == 1:           
                vendor_ref = self.env['purchase.order'].search([('name', '=', ori.group_id.name)])
                ori.custom_ref = vendor_ref.partner_ref