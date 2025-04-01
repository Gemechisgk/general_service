from odoo import models


class StudentData(models.AbstractModel):
    _name = "report.school.report_student_registration_wizard"

    def _get_report_values(self, docids, data=None):
        product_id = self.env['product.product'].search([])
        print(product_id)

        student_id = self.env['student.student'].search([('is_student', '=', True)])

        print(student_id)

        return {
            'doc_ids': docids,
            'docs': student_id,
            'data': data,
        }
