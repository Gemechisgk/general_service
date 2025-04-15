from odoo import models, api, fields
from datetime import datetime

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employment_duration = fields.Char(string='Duration of Employment', compute='_compute_employment_duration', store=True)

    @api.depends('create_date')
    def _compute_employment_duration(self):
        for employee in self:
            if employee.create_date:
                start_date = fields.Datetime.from_string(employee.create_date)
                today = datetime.now()
                delta = today - start_date
                years = delta.days // 365
                months = (delta.days % 365) // 30
                days = delta.days % 30
                
                duration_parts = []
                if years > 0:
                    duration_parts.append(f"{years} {'year' if years == 1 else 'years'}")
                if months > 0:
                    duration_parts.append(f"{months} {'month' if months == 1 else 'months'}")
                if days > 0 and years == 0:  # Only show days if less than a year
                    duration_parts.append(f"{days} {'day' if days == 1 else 'days'}")
                
                employee.employment_duration = ' '.join(duration_parts) if duration_parts else 'Less than a day'
            else:
                employee.employment_duration = 'N/A'

    def print_badge(self):
        self.ensure_one()
        return self.env.ref('hr.hr_employee_print_badge').report_action(self)

    def print_resume(self):
        self.ensure_one()
        return {
            'name': 'Print Resume',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.cv.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_ids': self.ids,
            }
        } 