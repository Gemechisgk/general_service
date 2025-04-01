from odoo import models, fields, api
from PIL import Image
from io import BytesIO


class ImageCard(models.Model):
    _name = 'image.card'
    _description = 'Image Card'
    name = fields.Char()
    phone = fields.Char()
    card_id = fields.Char()
    image = fields.Binary()
    receipt_image = fields.Binary()
    text = fields.Text()
