from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FuelRequest(models.Model):
    _name = 'fuel.request'
    _description = 'Fuel Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Request Number', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today, tracking=True)
    description = fields.Char(string='Description', required=True, tracking=True)
    previous_km_reading = fields.Float(string='Previous KM Reading', required=True, tracking=True)
    current_km_reading = fields.Float(string='Current KM Reading', required=True, tracking=True)
    km_difference = fields.Float(string='KM Difference', compute='_compute_km_difference', store=True)
    km_per_liter = fields.Float(string='KM/Liter', required=True, tracking=True)
    requested_liters = fields.Float(string='Requested Liters', compute='_compute_requested_liters', store=True)
    plate_number = fields.Char(string='Plate Number', required=True, tracking=True)
    requested_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, tracking=True)
    refueled_by = fields.Many2one('res.users', string='Refueled By', tracking=True)
    approved_by = fields.Many2one('res.users', string='Approved By', tracking=True)
    finance_approval = fields.Boolean(string='Finance Approval', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('refueled', 'Refueled'),
        ('done', 'Done')
    ], string='Status', default='draft', tracking=True)

    @api.depends('previous_km_reading', 'current_km_reading')
    def _compute_km_difference(self):
        for record in self:
            record.km_difference = record.current_km_reading - record.previous_km_reading

    @api.depends('km_difference', 'km_per_liter')
    def _compute_requested_liters(self):
        for record in self:
            if record.km_per_liter > 0:
                record.requested_liters = record.km_difference / record.km_per_liter
            else:
                record.requested_liters = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('fuel.request') or _('New')
        return super().create(vals_list)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_refuel(self):
        self.write({'state': 'refueled'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref('general_service.action_fuel_request_report').report_action(self) 