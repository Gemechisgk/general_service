from odoo import models, fields, api, _

class MaterialDistribution(models.Model):
    _name = 'material.distribution'
    _description = 'Material Distribution'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Distribution Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    date = fields.Date(string='Distribution Date', required=True, default=fields.Date.context_today, tracking=True)
    material = fields.Char(string='Material', required=True, tracking=True)
    employee_ids = fields.Many2many('hr.employee', string='Employees Receiving Material', tracking=True)
    amount = fields.Float(string='Amount', required=False, tracking=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('material.distribution') or _('New')
        return super().create(vals_list)

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref('general_service.action_material_distribution_report').report_action(self)

    @api.depends('employee_ids', 'amount')
    def _compute_employee_table(self):
        for rec in self:
            rec.employee_table = [
                {'name': emp.name, 'amount': rec.amount} for emp in rec.employee_ids
            ]

    employee_table = fields.Json(string='Employee Table', compute='_compute_employee_table', store=False)

class MaterialDistributionLine(models.Model):
    _name = 'material.distribution.line'
    _description = 'Material Distribution Line'

    distribution_id = fields.Many2one('material.distribution', string='Distribution', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    material = fields.Char(string='Material', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    notes = fields.Text(string='Notes') 