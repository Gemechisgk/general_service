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
        'security/employee_groups_security.xml',
        'security/ir.model.access.csv',
        'report/employee_registration_report.xml',
        'report/action_employee_report_wizard.xml',
        'report/analysis_report.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/employee_process_view.xml',
        'views/image_card_view.xml',
        'wizard/employee_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

