from odoo import models, fields, api


class ResUserLog(models.Model):

    _inherit = "res.users.log"

    longitude = fields.Char("Longitude")
    latitude = fields.Char("Latitude")
    address_mac = fields.Char("Address Mac")
