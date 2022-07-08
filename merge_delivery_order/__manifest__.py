# -*- coding: utf-8 -*-
{
    'name': "Merge Delivery Order",
    'summary': """merge delivery order""",
    'description': """""",
    'author': "My Company",
    'category': 'inventory',
    'version': '0.1',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/merge_delivery_order_wizard.xml',
        'report/delivery_report_merge.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
