# -*- coding: utf-8 -*-
{
    'name': "General Service",

    'summary': "General Service module to manage employees information",

    'description': """

    """,

    'author': "Infinity Advanced Technology",
    'website': "https://www.inifnity-et.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/students_groups_security.xml',
        'security/ir.model.access.csv',
        'report/student_registraion_report.xml',
        'report/action_student_report_wizard.xml',
        'report/analysis_report.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/students_process_view.xml',
        'views/image_card_view.xml',
        'wizard/student_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

