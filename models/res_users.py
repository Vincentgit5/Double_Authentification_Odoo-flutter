# -*- coding: utf-8 -*-
import json
import random
import xmlrpc

from my_addons.its_2f_authentication.tools import encrypt
from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = "res.users",

    its_identity_ids = fields.One2many('its.its_2f_authentication', inverse_name='user_id',
                                       domain=lambda self: [('user_id', '=', self.id)])
    user_mobile_code_pin = fields.Char(string='User Mobile Pin', copy=False, readonly=True, size=5)
    activate = fields.Boolean(string='Activate', default=True)
    custom_field = fields.Char(string='Custom Field')

    @api.multi
    def unique_number_generate(self):
        user_mobile_code_pin = ''.join(random.choices('0123456789', k=5))
        return self.write({'user_mobile_code_pin': user_mobile_code_pin})
        print(user_mobile_code_pin)

    _sql_constraints = [
        ('user_mobile_code_pin_unique', 'unique(user_mobile_code_pin)', _('Mobile unique pin already exist'))
    ]

    @api.multi
    def generate_user_public_and_private_keys(self):
        new_user_public_and_private_key = self.env['its.its_2f_authentication'].create({
            'name': _('User Keys'),
            'user_id': self.id,
        })
        new_user_public_and_private_key.generate_key()
        return self.write({'new_user_public_and_private_key': new_user_public_and_private_key})

    @api.multi
    def message_crypter(self):
        message = "yours code is user"
        encrypted_message = encrypt()
        return encrypted_message

