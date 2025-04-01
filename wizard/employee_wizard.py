import io

from odoo import models, fields


class EmployeeWizard(models.TransientModel):
    _name = "employee.registration.wizard"

    department_id = fields.Many2one("employee.departments", string="Department Name", )

    def print_report(self):
        data = {'department_id': self.department_id}
        return self.env.ref('general_service.action_employee_report_wizard').report_action([], data=data)

