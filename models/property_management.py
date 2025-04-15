from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class PropertyManagement(models.Model):
    _name = 'property.management'
    _description = 'Property Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Property Name', required=True, tracking=True)
    property_id = fields.Char(string='Property ID', required=True, copy=False, readonly=True, 
                            default=lambda self: _('New'))
    location = fields.Text(string='Location', required=True, tracking=True)
    property_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('land', 'Land'),
        ('other', 'Other')
    ], string='Property Type', required=True, tracking=True)
    acquisition_date = fields.Date(string='Acquisition Date', required=True, tracking=True)
    current_value = fields.Float(string='Current Value', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', 
                               default=lambda self: self.env.company, required=True)
    ownership_history_ids = fields.One2many('property.ownership.history', 'property_id', 
                                          string='Ownership History', readonly=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Documents')
    notes = fields.Text(string='Notes')
    barcode = fields.Char(string='Barcode', compute='_compute_barcode', store=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='draft', tracking=True)

    @api.depends('property_id')
    def _compute_barcode(self):
        for record in self:
            if record.property_id:
                # Ensure the barcode is a valid value (alphanumeric without spaces)
                # Replace any spaces or special characters with dashes
                barcode_value = record.property_id.replace(' ', '-')
                # Ensure the barcode is not empty by adding a prefix if needed
                if not barcode_value or barcode_value == 'New':
                    barcode_value = f"PROP-{record.id or '0'}"
                record.barcode = barcode_value
            else:
                record.barcode = f"PROP-{record.id or '0'}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('property_id', _('New')) == _('New'):
                vals['property_id'] = self.env['ir.sequence'].next_by_code('property.management') or _('New')
        return super().create(vals_list)

    def action_print_property_id(self):
        self.ensure_one()
        return self.env.ref('general_service.action_property_id_report').report_action(self)

class PropertyOwnershipHistory(models.Model):
    _name = 'property.ownership.history'
    _description = 'Property Ownership History'
    _order = 'transfer_date desc'

    property_id = fields.Many2one('property.management', string='Property', required=True, ondelete='cascade')
    transfer_date = fields.Date(string='Transfer Date', required=True)
    transfer_document = fields.Binary(string='Transfer Document')
    transfer_document_name = fields.Char(string='Document Name')
    notes = fields.Text(string='Notes') 