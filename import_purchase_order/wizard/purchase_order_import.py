from odoo import api, models, fields


class PurchaseOrderImportWizard(models.TransientModel):
    _name = "purchase.order.import.wizard"

    partner_id = fields.Many2one('res.partner', string='Client', required=True, domain=[('supplier_rank', '>=', 0)])
    product_list = fields.One2many('purchase.order.import', 'product_id',
                                   string="Product")


    def po_import(self):
        print("okie!")


