import logging
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError  # استيراد ValidationError

# إنشاء كائن logger
_logger = logging.getLogger(__name__)


class Student(models.Model):
    _name = "student.student"
    _description = "Student"

    name = fields.Char(string="Student Name", )
    amount = fields.Float(string="Fees", )
    department_id = fields.Many2one("student.departments", string="Department Name", )
    subject_ids = fields.Many2many("student.subjects", "subject_student_rel", string="Subjects")
    result_student_ids = fields.One2many("student.result", "student_id", string="Results")
    age = fields.Integer(string="Age", compute="get_age", store=True)
    date_of_birth = fields.Date(string="Date of Birth", )
    is_student = fields.Boolean(string="Is Student", default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    image = fields.Image(string="Student Image", max_width=128, max_height=128)

    @api.depends("date_of_birth")
    def get_age(self):
        """
        Computes the age of the student based on their date of birth.
        The age is computed as the difference between the current date and
        the student's date of birth.
        """
        for student in self:
            if student.date_of_birth:
                today = date.today()
                birth_date = fields.Date.from_string(student.date_of_birth)
                delta = relativedelta(today, birth_date)
                student.age = delta.years
                _logger.info(f"Calculated age for student {student.name}: {student.age} years")  # تسجيل العمر المحسوب
            else:
                student.age = 0  # If no birth date is provided, age is set to 0
                _logger.warning(f"No date of birth provided for student {student.name}. Age set to 0.")  # تسجيل تحذير
    @api.model
    def create_product(self, id=None):
        """
        دالة لإنشاء منتج جديد
        """
        # قيم افتراضية
        product_name = "New Product2"
        product_price = 150.0

        # تسجيل بدء عملية إنشاء المنتج
        _logger.info(f"Starting to create product with name: {product_name} and price: {product_price}")

        # إنشاء منتج جديد
        product = self.env['product.product'].create({
            'name': product_name,  # اسم المنتج
            'list_price': product_price,  # سعر المنتج
            'type': 'service',  # نوع المنتج (يمكن تغييره إلى 'product' أو 'consu')
        })

        # تسجيل نجاح عملية إنشاء المنتج
        _logger.info(f"Product created successfully with ID: {product.id}")

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'res_id': product.id,
            'view_mode': 'form',
            'target': 'current',
        }


class Departments(models.Model):
    _name = "student.departments"
    _description = "Department"

    name = fields.Char(string="Department Name", )
    address = fields.Char(string="Address")


class Subjects(models.Model):
    _name = "student.subjects"
    _description = "Subject"

    name = fields.Char(string="Subject Name", )


class Result(models.Model):
    _name = "student.result"
    _description = "Student Result"

    student_id = fields.Many2one("student.student", string="Student", )
    result = fields.Float(string="Result", )
    subject_id = fields.Many2one("student.subjects", string="Subject", )

    @api.constrains('result')
    def check_result_range(self):
        """
        Ensures that the result is between 0 and 100.
        """
        for record in self:
            if not (0 <= record.result <= 100):
                raise ValidationError("Result must be between 0 and 100.")
# 1:35
