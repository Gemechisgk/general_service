from odoo import models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def print_badge(self):
        self.ensure_one()
        return self.env.ref('hr.hr_employee_print_badge').report_action(self)

    def print_resume(self):
        self.ensure_one()
        return self.env.ref('hr.report_employee_resume').report_action(self) 