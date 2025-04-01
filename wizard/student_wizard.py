import io

from odoo import models, fields


class StudentWizard(models.TransientModel):
    _name = "student.registration.wizard"

    department_id = fields.Many2one("student.departments", string="Department Name", )

    def print_report(self):
        data = {'department_id': self.department_id}
        return self.env.ref('school.action_student_report_wizard').report_action([], data=data)

