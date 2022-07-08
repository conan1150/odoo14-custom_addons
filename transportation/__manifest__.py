# -*- coding: utf-8 -*-
{
    'name': "Transportation",
    'summary': """Container management and shipping tracking modules.""",
    'description': """Container management.""",
    'author': "My Company",
    'category': 'Purchase',
    'version': '0.1',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/containers_views.xml',
        # 'views/configurations_views.xml',
        'views/transportation_views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
