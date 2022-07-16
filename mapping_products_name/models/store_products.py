from odoo import models, fields, api, _


class store_products(models.Model):
    _name = 'store.products'
    _description = 'mapping_product_name.store_product'

    name = fields.Char('Name', required=True)
    # store_id = fields.Many2one('store.list', string='Store', required=True)

    store_product_variant_ids = fields.One2many('store.products.variant', 'store_product_id', string='Variations Code')
    store_product_variant_id = fields.Many2one('store.products.variant', 'Product', compute='_compute_store_product_variant_id')

    store_product_default_code = fields.Char(
        'Internal Reference', compute='_compute_store_product_default_code',
        inverse='_set_store_product_default_code', store=True)
   
    @api.depends('store_product_variant_ids')
    def _compute_store_product_variant_id(self):
        for p in self:
            p.store_product_variant_id = p.store_product_variant_ids[:1].id

    @api.depends('store_product_variant_ids', 'store_product_variant_ids.store_product_default_code')
    def _compute_store_product_default_code(self):
        unique_variants = self.filtered(lambda template: len(template.store_product_variant_ids) == 1)
        for template in unique_variants:
            template.store_product_default_code = template.store_product_variant_ids.store_product_default_code
        for template in (self - unique_variants):
            template.store_product_default_code = False 


    def _set_store_product_default_code(self):
        for template in self:
            if len(template.store_product_variant_ids) == 1:
                template.store_product_variant_ids.store_product_default_code = template.store_product_default_code


class store_products_variant(models.Model):
    _name = 'store.products.variant'
    _description = 'mapping_product_name.store_products_variant'

    name = fields.Char('Name')
    store_product_id = fields.Many2one('store.products', string='Product')
    store_product_default_code = fields.Char('Internal Reference', index=True)
    store_product_sub_code = fields.Char('Reference')


class map_product_to_other_stores(models.Model):
    _name = 'map.product.to.other.stores'
    _description = 'map_product_to_other_stores'
    
    name = fields.Char('Sub Code')


class Stores(models.Model):
    _inherit = 'store.list'


class Products(models.Model):
    _inherit = 'product.product'


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_product_by_store_action(self):
        action = {
            'name': _('Product By Store'),
            'res_model': 'store.products',
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'list,form',            
            # 'context': ctx,
            # 'domain': domain or [],
        }

        action['view_id'] = self.env.ref('mapping_products_name.product_by_store_view_tree').id
        form_view = self.env.ref('mapping_products_name.product_by_store_view_tree').id

        action.update({
            'views': [
                (action['view_id'], 'list'),
                (form_view, 'form'),
            ],
        })

        return action

