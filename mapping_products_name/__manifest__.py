# -*- coding: utf-8 -*-
{
    'name': "Products Name Mapping",
    'summary': """Associate product names within the system with different product names from multiple stores.""",
    'description': """""",
    'author': "IV",
    'category': 'product',
    'version': '0.1',
    'depends': ['base', 'stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',

        'views/store.xml',
        'views/product_by_stores.xml',
        'views/btn_store_product_extended.xml',

        'wizard/open_import_update_product_list_wiz.xml',
        'wizard/import_sale_order_wiz.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
