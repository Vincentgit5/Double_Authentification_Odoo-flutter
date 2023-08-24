# -*- coding: utf-8 -*-
import json
import xmlrpc.client
from random import random


from odoo import models, fields, api, _
from my_addons.its_2f_authentication.tools import generate_key_pair, generate_number, generer_numero, encrypt


class its_identity_user(models.Model):
    _name = 'its.its_2f_authentication'
    _order = 'create_date DESC'

    date = fields.Datetime('Date', required=True, default=fields.Datetime.now)
    validation_date = fields.Datetime('Validation date')
    user_validation = fields.Many2one(comodel_name='res.users', string="User validation")
    private_key = fields.Char('Private key')
    public_key = fields.Char('Public key')
    description = fields.Text("Type your text")
    users_id = fields.Many2one(comodel_name='res.users', string='User', required=True,
                               default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id,
                                 ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User')
    state = fields.Selection([('draft', 'Draft'), ('validate', 'Validate')])
    reference_no = fields.Char(string='Sequence Number', required=True,
                               readonly=True, default=lambda self: _('New'))
    user_key_ids = fields.Many2many(comodel_name='res.users')
    user_mobile_code_pin = fields.Char(string='User Mobile Pin', copy=False, readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'users.rec') or _('New')
        res = super(its_identity_user, self).create(vals)
        return res

    @api.multi
    def next_level(self):
        if self.state == 'draft':
            return self.write({'state': 'validate'})

    @api.multi
    def name_get(self):
        result = []
        for user_key in self:
            name = str(user_key.user_id.name) + ': ' + str(user_key.public_key)
            result.append((user_key.id, name))
        return result

    @api.multi
    def generate_key(self):
        keys = generate_key_pair()
        key1 = keys[0]
        key2 = keys[1]
        public_key = '{}:{}'.format(key1[0], key1[1])
        private_key = '{}:{}'.format(key2[0], key2[1])
        return self.write({'private_key': private_key, 'public_key': public_key})

    @api.one
    def unique_number_generates(self):
        user_mobile_code = str(random.randint(10000, 99999))
        return user_mobile_code

    _sql_constraints = [
        ('user_mobile_code', 'unique(user_mobile_code)', 'The value of My Field must be unique.'),
    ]

