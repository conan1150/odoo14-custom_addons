# -*- coding: utf-8 -*-
{
    'name': "Import Purchase Order",
    'summary': """Import Purchase Order Item By Order""",
    'description': """""",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/purchase_order_import.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
