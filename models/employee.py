import logging
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class Employee(models.Model):
    _name = "employee.employee"
    _description = "Employee"
    _rec_name = "name"

    name = fields.Many2one("hr.employee", string="Employee Name", required=True)
    department_id = fields.Many2one("hr.department", string="Department Name")
    age = fields.Integer(string="Age", compute="get_age", store=True)
    date_of_birth = fields.Date(string="Date of Birth")
    is_employee = fields.Boolean(string="Is Employee", default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    image = fields.Image(string="Employee Image", max_width=128, max_height=128)

    @api.depends("date_of_birth")
    def get_age(self):
        for employee in self:
            if employee.date_of_birth:
                today = date.today()
                birth_date = fields.Date.from_string(employee.date_of_birth)
                delta = relativedelta(today, birth_date)
                employee.age = delta.years
                _logger.info(f"Calculated age for employee {employee.name.name if employee.name else 'Unnamed'}: {employee.age} years")
            else:
                employee.age = 0
                _logger.warning(f"No date of birth provided for employee {employee.name.name if employee.name else 'Unnamed'}. Age set to 0.")

    @api.onchange('name')
    def _onchange_name(self):
        if self.name and self.name.department_id:
            self.department_id = self.name.department_id
        else:
            self.department_id = False

    @api.model
    def create_id(self, vals=None):
        _logger.info(f"create_id called with context: {self.env.context}")
        _logger.info(f"Current record ID: {self.id if self else 'New'}, Name: {self.name.name if self.name else 'None'}, Department: {self.department_id.name if self.department_id else 'None'}")
        
        # Check if name is set; raise an error if not
        if not self.name:
            raise UserError("Cannot create a new employee without selecting an Employee Name first.")
        
        new_employee_vals = {
            'name': self.name.id,  # Guaranteed to be set due to the check above
            'department_id': self.department_id.id if self.department_id else False,
            'is_employee': True,
            'company_id': self.env.company.id,
        }
        
        with self.env.cr.savepoint():
            new_employee = self.env['employee.employee'].sudo().create(new_employee_vals)
        
        _logger.info(f"New employee created successfully with ID: {new_employee.id}")
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.employee',
            'res_id': new_employee.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def unlink(self):
        _logger.error(f"Attempting to delete employee records: {self.ids}")
        raise ValidationError(f"Deletion blocked for debugging. Attempted to delete records: {self.ids}")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.name.display_name:
                record.display_name = record.name.display_name
            else:
                record.display_name = "Unnamed Employee"