# -*- coding: utf-8 -*-
{
    'name': "Products Name Mapping",
    'summary': """Associate product names within the system with different product names from multiple stores.""",
    'description': """""",
    'author': "IV",
    'category': 'product',
    'version': '0.1',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',

        'views/store.xml',
        'views/store_products.xml',
        'views/product_extended.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
