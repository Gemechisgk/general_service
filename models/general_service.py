from odoo import models, fields

class GeneralService(models.Model):
    _name = 'general_service.general_service'
    _description = 'General Service'

    name = fields.Char(string='Name')
    value = fields.Integer(string='Value')
    value2 = fields.Float(string='Value 2') 