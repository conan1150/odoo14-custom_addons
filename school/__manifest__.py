{
    'name' : 'School',
    'version': '1.0',
    'author': 'INTIRA',
    'summary': 'School Management System',
    'sequnece': 1,
    'description': "This is school management system software suppored in 'Odoo v14'",
    'category': "School",
    'website': 'https://www.odoo.com/page/school',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/school_view.xml',

        'data/school_data.xml'
    ],
    'demo': [
        'demo/school_demo.xml'
    ]
}
