from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_import_order_list(self):
        return self.env['ir.actions.act_window']._for_xml_id("mapping_products_name.import_sale_order_list_wizard_action")