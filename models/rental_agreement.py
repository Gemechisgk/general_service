from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class RentalAgreement(models.Model):
    _name = 'rental.agreement'
    _description = 'Rental Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Agreement Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    property_owner_id = fields.Many2one('res.partner', string='Property Owner', required=True, tracking=True)
    property_address = fields.Text(string='Property Address', required=True, tracking=True)
    rental_amount = fields.Float(string='Monthly Rental Amount', required=True, tracking=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    notes = fields.Text(string='Notes')
    version = fields.Integer(string='Version', default=1)
    previous_version_ids = fields.One2many('rental.agreement.version', 'current_agreement_id', string='Previous Versions')
    reminder_days = fields.Integer(string='Reminder Days', default=30, 
                                 help='Number of days before contract expiry to send reminder')
    last_reminder_date = fields.Date(string='Last Reminder Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', 
                               default=lambda self: self.env.company, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('rental.agreement') or _('New')
        return super().create(vals_list)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for agreement in self:
            if agreement.start_date and agreement.end_date:
                if agreement.start_date > agreement.end_date:
                    raise ValidationError(_('End date must be after start date.'))

    def action_confirm(self):
        self.write({'state': 'active'})
        self._schedule_expiry_reminder()

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_renew(self):
        self.ensure_one()
        new_agreement = self.copy({
            'version': self.version + 1,
            'state': 'draft',
            'previous_version_ids': [(0, 0, {
                'agreement_id': self.id,
                'version': self.version,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'rental_amount': self.rental_amount,
            })],
        })
        return {
            'name': _('New Rental Agreement'),
            'type': 'ir.actions.act_window',
            'res_model': 'rental.agreement',
            'view_mode': 'form',
            'res_id': new_agreement.id,
            'target': 'current',
        }

    def _schedule_expiry_reminder(self):
        for agreement in self:
            if agreement.state == 'active' and agreement.end_date:
                reminder_date = agreement.end_date - timedelta(days=agreement.reminder_days)
                if reminder_date > fields.Date.today():
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'note': _('Rental Agreement %s is expiring on %s') % (agreement.name, agreement.end_date),
                        'user_id': self.env.user.id,
                        'res_id': agreement.id,
                        'res_model_id': self.env['ir.model']._get('rental.agreement').id,
                        'date_deadline': reminder_date,
                    })

    def action_print_agreement(self):
        return self.env.ref('general_service.action_report_rental_agreement').report_action(self)

class RentalAgreementVersion(models.Model):
    _name = 'rental.agreement.version'
    _description = 'Rental Agreement Version History'

    current_agreement_id = fields.Many2one('rental.agreement', string='Current Agreement')
    agreement_id = fields.Many2one('rental.agreement', string='Previous Agreement')
    version = fields.Integer(string='Version')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    rental_amount = fields.Float(string='Rental Amount')
    changed_by = fields.Many2one('res.users', string='Changed By')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)