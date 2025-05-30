# -*- coding: utf-8 -*-
{
    'name': "General Service",

    'summary': "General Service module to manage employees information",

    'description': """
        This module provides general service management features including:
        - Employee management
        - Rental agreement management
        - Property management
        - Fuel request management
        - Employee document printing
        - Airplane ticket requests
        - Vehicle travel requests
    """,

    'author': "Infinity Advanced Technology",
    'website': "https://www.inifnity-et.com",

    'category': 'Services',
    'version': '1.0',

    'depends': ['base', 'hr', 'mail', 'fleet'],

    'data': [
        'security/employee_groups_security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/airplane_ticket_sequence.xml',
        'data/vehicle_request_sequence.xml',
        'views/menu_icon.xml',
        'report/employee_registration_report.xml',
        'report/action_employee_report_wizard.xml',
        'report/analysis_report.xml',
        'report/employee_badge_report.xml',
        'report/employee_documents.xml',
        'report/rental_agreement_report.xml',
        'report/employee_resume_report.xml',
        'report/property_id_report.xml',
        'report/fuel_request_report.xml',
        'report/vehicle_request_report.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/employee_process_view.xml',
        'views/employee_document_print.xml',
        'wizard/employee_wizard.xml',
        'views/rental_agreement_view.xml',  
        'views/property_management_view.xml',
        'views/property_ownership_history_view.xml',
        'views/fuel_request_view.xml',
        'wizard/hr_employee_cv_wizard_view.xml',
        'views/material_distribution_view.xml',
        'report/material_distribution_report.xml',
        'views/airplane_ticket_view.xml',
        'report/airplane_ticket_report.xml',
        'views/vehicle_request_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

