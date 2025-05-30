from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AirplaneTicket(models.Model):
    _name = 'airplane.ticket'
    _description = 'Airplane Ticket Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Request Number', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    
    # Requester Details
    requester_id = fields.Many2one('hr.employee', string='Full Name', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True, tracking=True)
    contact_number = fields.Char(string='Contact Number', required=True, tracking=True)
    reason_for_travel = fields.Text(string='Reason for Travel', required=True, tracking=True)
    origin = fields.Char(string='Origin', required=True, tracking=True)
    destination = fields.Char(string='Destination', required=True, tracking=True)
    
    # Travel Details
    travel_type = fields.Selection([
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip')
    ], string='Travel Type', required=True, default='one_way', tracking=True)
    
    # Travel Agent/Contract Details
    travel_agent_id = fields.Many2one('res.partner', string='Travel Agent', required=True, tracking=True)
    contract_reference = fields.Char(string='Contract Reference', tracking=True)
    flight_number = fields.Char(string='Flight Number', tracking=True)
    departure_date = fields.Date(string='Departure Date', required=True, tracking=True)
    departure_time = fields.Float(string='Departure Time', tracking=True)
    return_date = fields.Date(string='Return Date', tracking=True)
    ticket_price = fields.Float(string='Ticket Price', tracking=True)
    
    # Attachments
    flight_details_attachment = fields.Binary(string='Flight Details Document', attachment=True)
    flight_details_filename = fields.Char(string='Flight Details Filename')
    
    # Hidden Approval Fields (for report only)
    approved_by = fields.Many2one('res.users', string='Approved By', tracking=True)
    approval_date = fields.Date(string='Approval Date', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked', 'Booked'),
        ('completed', 'Completed')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', 
                               default=lambda self: self.env.company, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('airplane.ticket') or _('New')
        return super().create(vals_list)

    @api.onchange('requester_id')
    def _onchange_requester_id(self):
        if self.requester_id:
            self.department_id = self.requester_id.department_id

    @api.constrains('departure_date', 'return_date')
    def _check_dates(self):
        for record in self:
            if record.travel_type == 'round_trip' and record.return_date:
                if record.departure_date > record.return_date:
                    raise ValidationError(_('Return date must be after departure date.'))

    def action_submit(self):
        self.write({'state': 'booked'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_print_request(self):
        self.ensure_one()
        return self.env.ref('general_service.action_report_airplane_ticket').report_action(self) 