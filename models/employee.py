import logging
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError  


_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _name = "employee.employee"
    _description = "Employee"

    name = fields.Char(string="Employee Name", )
    amount = fields.Float(string="Fees", )
    department_id = fields.Many2one("employee.departments", string="Department Name", )
    subject_ids = fields.Many2many("employee.subjects", "subject_employee_rel", string="Subjects")
    result_employee_ids = fields.One2many("employee.result", "employee_id", string="Results")
    age = fields.Integer(string="Age", compute="get_age", store=True)
    date_of_birth = fields.Date(string="Date of Birth", )
    is_employee = fields.Boolean(string="Is Employee", default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    image = fields.Image(string="Employee Image", max_width=128, max_height=128)

    @api.depends("date_of_birth")
    def get_age(self):
        """
        Computes the age of the employee based on their date of birth.
        The age is computed as the difference between the current date and
        the employee's date of birth.
        """
        for employee in self:
            if employee.date_of_birth:
                today = date.today()
                birth_date = fields.Date.from_string(employee.date_of_birth)
                delta = relativedelta(today, birth_date)
                employee.age = delta.years
                _logger.info(f"Calculated age for employee {employee.name}: {employee.age} years") 
            else:
                employee.age = 0  # If no birth date is provided, age is set to 0
                _logger.warning(f"No date of birth provided for employee {employee.name}. Age set to 0.") 
    @api.model
    def create_product(self, id=None):
     
        product_name = "New Product2"
        product_price = 150.0

        _logger.info(f"Starting to create product with name: {product_name} and price: {product_price}")

        product = self.env['product.product'].create({
            'name': product_name,  
            'list_price': product_price,  
            'type': 'service',  
        })

        
        _logger.info(f"Product created successfully with ID: {product.id}")

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'res_id': product.id,
            'view_mode': 'form',
            'target': 'current',
        }


class Departments(models.Model):
    _name = "employee.departments"
    _description = "Department"

    name = fields.Char(string="Department Name", )
    address = fields.Char(string="Address")


class Subjects(models.Model):
    _name = "employee.subjects"
    _description = "Subject"

    name = fields.Char(string="Subject Name", )


class Result(models.Model):
    _name = "employee.result"
    _description = "Employee Result"

    employee_id = fields.Many2one("employee.employee", string="Employee", )
    result = fields.Float(string="Result", )
    subject_id = fields.Many2one("employee.subjects", string="Subject", )

    @api.constrains('result')
    def check_result_range(self):
        """
        Ensures that the result is between 0 and 100.
        """
        for record in self:
            if not (0 <= record.result <= 100):
                raise ValidationError("Result must be between 0 and 100.")
