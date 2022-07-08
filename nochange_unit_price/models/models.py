# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # o_unit_price = fields.float(related='price_unit')

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        o_price = self.o_unit_price
        sup = super(PurchaseOrderLine, self)._onchange_quantity()
        self.o_unit_price = o_price

        return sup
