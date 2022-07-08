# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderImport(models.Model):
    _name = "purchase.order.import"

    product_id = fields.Many2one("product.product", string="Product")
    number_of_containers = fields.Integer("Containers.")


# class ProductPerContainer(models.Model):
#     _inherit = 'product.product'
#
#     product_per_container = fields.Intiger("Product Per Container.")