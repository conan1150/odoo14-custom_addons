# -*- coding: utf-8 -*-
{
    'name': "School Inherit Views",
    'summary': """
        Creating different Inheritance test case""",
    'description': """
        Creating different Inheritance test case
    """,
    'author': "FoxDev.",
    'category': 'School',
    'version': '0.1',
    'depends': ['base', 'school', 'school_student'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/student_extend.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
