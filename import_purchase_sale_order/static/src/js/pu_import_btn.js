odoo.define('import_purchase_sale_order.pu_import_btn', function (require) {
    "use strict";
    
var core = require('web.core');
// var ListView = require('web.ListView');
var ListController = require('web.ListController');
var QWeb = core.qweb;
var _t = core._t;
 
 
ListController.include({       
     
    renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
              this.$buttons.find('.o_button_pu_import').click(this.proxy('wiz_purchase_import_action'));
              this.$buttons.find('.o_button_sale_import').click(this.proxy('wiz_sale_import_action'));
            }            
    },
    wiz_purchase_import_action: function () {
        var self =this;
        self.do_action({
                    name: _t('Import RFQ (code, quantity, price) .XLS(x)'),
                    type: 'ir.actions.act_window',
                    res_model: 'purchase.order.import.wizard',
                    views: [[false, 'form']],
                    view_mode: 'form',
                    target: 'new',
                });
        return { 'type': 'ir.actions.act_window',
                'tag': 'reload',
        } 
    },
    wiz_sale_import_action: function () {
        var self =this;
        self.do_action({
                    name: _t('Import quotation (code, quantity, price) .XLS(x)'),
                    type: 'ir.actions.act_window',
                    res_model: 'sale.order.import.wizard',
                    views: [[false, 'form']],
                    view_mode: 'form',
                    target: 'new',
                });
        return { 'type': 'ir.actions.act_window',
                'tag': 'reload',
        } 
    }
});
});