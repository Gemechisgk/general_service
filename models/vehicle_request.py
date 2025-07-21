from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class VehicleRequest(models.Model):
    _name = 'vehicle.request'
    _description = 'Vehicle Travel Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Request Number', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    
    # Requester Details
    requester_id = fields.Many2one('hr.employee', string='Full Name', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True, tracking=True)
    contact_number = fields.Char(string='Contact Number', required=True, tracking=True)
    
    # Travel Details
    travel_datetime = fields.Datetime(string='Date and Time of Travel', required=True, tracking=True)
    destination = fields.Char(string='Destination', required=True, tracking=True)
    purpose = fields.Text(string='Purpose of Travel', required=True, tracking=True)
    odometer_start = fields.Float(string='Odometer Reading Start', tracking=True)
    odometer_end = fields.Float(string='Odometer Reading Return', tracking=True)
    distance_traveled = fields.Float(string='Distance Traveled', compute='_compute_distance_traveled', store=True)
    
    # Vehicle Assignment
    vehicle_id = fields.Many2one('fleet.vehicle', string='Assigned Vehicle', tracking=True)
    driver_id = fields.Many2one('hr.employee', string="Driver's Name", tracking=True)
    plate_number = fields.Char(related='vehicle_id.license_plate', string='Plate Number', store=True)
    expected_return_datetime = fields.Datetime(string='Expected Return Date & Time', tracking=True)
    actual_return_datetime = fields.Datetime(string='Actual Return Date & Time', tracking=True)
    
    # Hidden Approval Fields (for report only)
    department_head_id = fields.Many2one('hr.employee', string='Department Head', tracking=True)
    dept_approval_date = fields.Date(string='Department Approval Date', tracking=True)
    service_head_id = fields.Many2one('hr.employee', string='General Service Head', tracking=True)
    service_approval_date = fields.Date(string='Service Head Approval Date', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('in_use', 'In Use'),
        ('returned', 'Returned')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', 
                               default=lambda self: self.env.company, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.request') or _('New')
        return super().create(vals_list)

    @api.depends('odometer_start', 'odometer_end')
    def _compute_distance_traveled(self):
        for record in self:
            if record.odometer_start and record.odometer_end:
                record.distance_traveled = record.odometer_end - record.odometer_start
            else:
                record.distance_traveled = 0.0

    @api.onchange('requester_id')
    def _onchange_requester_id(self):
        if self.requester_id:
            self.department_id = self.requester_id.department_id

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.odometer_start = self.vehicle_id.odometer

    @api.constrains('odometer_start', 'odometer_end')
    def _check_odometer_values(self):
        for record in self:
            if record.odometer_end and record.odometer_start and record.odometer_end < record.odometer_start:
                raise ValidationError(_('Odometer Reading Return must be greater than or equal to Odometer Reading Start.'))

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_start_trip(self):
        if not self.odometer_start:
            raise ValidationError(_('Please enter the starting odometer reading.'))
        self.write({'state': 'in_use'})

    def action_return(self):
        if not self.odometer_end:
            raise ValidationError(_('Please enter the return odometer reading.'))
        if self.odometer_end < self.odometer_start:
            raise ValidationError(_('Return odometer reading cannot be less than starting reading.'))
        self.write({
            'state': 'returned',
            'actual_return_datetime': fields.Datetime.now()
        })

    def action_print_request(self):
        self.ensure_one()
        return self.env.ref('general_service.action_report_vehicle_request').report_action(self) 