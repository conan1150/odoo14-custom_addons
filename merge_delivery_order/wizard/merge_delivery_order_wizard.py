from odoo import api, models, fields
from re import search


class MergeDeliveryOrderLine(models.TransientModel):
    _name = 'delivery.order.merge.line'
    _description = 'Merge Delivery Order Line'
    _order = 'min_id asc'

    wiz_id = fields.Many2one('stock.merge.delivery.order.wizard', 'Wizard')
    min_id = fields.Integer('MinID')
    aggr_ids = fields.Char('Ids', required=True)


class StockMergeDeliveryOrderWizard(models.TransientModel):
    _name = 'stock.merge.delivery.order.wizard'    

    @api.model
    def default_get(self, fields):
        res = super(StockMergeDeliveryOrderWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids')

        res['order_ids'] = self.env['stock.picking'].browse(active_ids)
        res['partner_ids'] = self.env['stock.picking'].browse(active_ids).partner_id
        res['product_ids'] = self.env['stock.picking'].browse(active_ids).move_line_ids_without_package

        return res  

    order_ids = fields.Many2many('stock.picking', string='Delivery Order')
    partner_ids = fields.Many2many('res.partner', string='Customers')
    product_ids = fields.Many2many('stock.move.line', string='Product')
    

    def action_report_merge_order(self):
        delivery_list = [i.name for i in self.order_ids]

        order_lines = []

        for i in self.product_ids:
            if i.product_id.display_name not in [p['product_name'] for p in order_lines]:
                line = {
                        'product_name': i.product_id.display_name,
                        'order_no': f'{i.reference}' if i.origin is False else f'{i.reference}/{i.origin}',
                        'qty': i.product_uom_qty,
                        'location': i.location_id.name
                    }                
                order_lines.append(line)
            else:
                order_index = next((index for (index, d) in enumerate(order_lines) if d["product_name"] == i.product_id.display_name), None)
                order_lines[order_index]['order_no'] += "" if search(f'{i.reference}/{i.origin}', order_lines[order_index]['order_no']) else f', {i.reference}/{i.origin}'
                order_lines[order_index]['qty'] += i.product_uom_qty
                order_lines[order_index]['location'] += "" if search(i.location_id.name, order_lines[order_index]['location']) else f', {i.location_id.name}'
                # order_lines[order_index]['location'] += "" if i.location_id.name == order_lines[order_index]['location'] else f", {i.location_id.name}"


        for p in order_lines:
            p['qty'] = '{:,.0f}'.format(p['qty'])


        data = {'order_lines': order_lines,
                'partner_ids': [i.display_name for i in self.partner_ids]}

        return self.env.ref('merge_delivery_order.delivery_order_merge_action').report_action(self, data=data)