from odoo import models


class EmployeeData(models.AbstractModel):
    _name = "report.general_service.report_employee_registration_wizard"

    def _get_report_values(self, docids, data=None):
        product_id = self.env['product.product'].search([])
        print(product_id)

        employee_id = self.env['employee.employee'].search([('is_employee', '=', True)])

        print(employee_id)

        return {
            'doc_ids': docids,
            'docs': employee_id,
            'data': data,
        }
