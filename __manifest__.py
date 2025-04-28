# -*- coding: utf-8 -*-
{
    'name': "General Service",

    'summary': "General Service module to manage employees information",

    'description': """
        This module provides general service management features including:
        - Employee management
        - Rental agreement management
        - Property management
    """,

    'author': "Infinity Advanced Technology",
    'website': "https://www.inifnity-et.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'mail'],

    # always loaded
    'data': [
        'security/employee_groups_security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/menu_icon.xml',
        'report/employee_registration_report.xml',
        'report/action_employee_report_wizard.xml',
        'report/analysis_report.xml',
        'report/employee_badge_report.xml',
        'report/rental_agreement_report.xml',
        'report/employee_resume_report.xml',
        'report/property_id_report.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/rental_agreement_view.xml',  
        'views/employee_process_view.xml',  
        'views/property_management_view.xml',
        'views/property_ownership_history_view.xml',
        'wizard/employee_wizard.xml',
        'wizard/hr_employee_cv_wizard_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

