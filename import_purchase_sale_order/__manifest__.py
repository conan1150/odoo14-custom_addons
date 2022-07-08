# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Import Purchase / Sale Order lines .XLS(x)',
    'version': '1.0.1',
    'author': 'Odoo Dev',
    'website': '',
    'license': 'AGPL-3',
    'category': 'Sales,Purchase',
    'summary': "Import a purchase & a sale order from an .xls/.xlsx file Odoo V14",
    'depends': ['base',
                'sale',
                'purchase',
                'web'
                ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wiz_import_purchase_order.xml',
        'wizard/wiz_import_sale_order.xml',
        'views/purchase_import_btn.xml'
    ],

    'qweb': ['static/src/xml/pu_import_btn.xml'],
    # 'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'demo': [],
    'test': []
}
