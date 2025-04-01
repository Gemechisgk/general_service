from odoo import models, fields, api

class RentalAgreement(models.Model):
    _name = 'rental.agreement'
    _description = 'Rental Agreement'

    name = fields.Char(string='Agreement Name')