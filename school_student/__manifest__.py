# -*- coding: utf-8 -*-
{
    'name': "school_student",

    'summary': """This is student in school""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'school',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/school_student.xml',
        'views/school_hobby.xml',
        'views/school_car.xml',

        'wizard/student_fees_update_wizard.xml',

        'data/hobby.csv',
        'data/school.profile.csv',
        'data/school.student.csv',
        'data/student_data.xml',
        'data/del_student_record.xml',
        'data/student_noupdate.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
