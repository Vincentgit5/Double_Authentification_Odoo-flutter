# -*- coding: utf-8 -*-

from odoo import http, _
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from random import sample


class its_user_controller(http.Controller):

    @http.route('/User/user_private_key/<string:user_mobile_code_pin>', type='http', auth='public', cors='*')
    def send_user_private_key_notification(self, user_mobile_code_pin):
        user = http.request.env['res.users'].sudo().search([('user_mobile_code_pin', '=', user_mobile_code_pin)],
                                                           limit=1)
        if user and user.its_identity_ids:
            private_key = user.its_identity_ids[0].private_key
            user_private_key_parts = private_key.split(':')
            user_private_key_part1 = user_private_key_parts[0] if len(user_private_key_parts) > 0 else ""
            user_private_key_part2 = user_private_key_parts[1] if len(user_private_key_parts) > 1 else ""

            result = {
                'user_private_key_part1': user_private_key_part1,
                'user_private_key_part2': user_private_key_part2,
            }
            return json.dumps(result)

        elif user and (not user.its_identity_ids or not user.its_identity_ids.private_key):
            return json.dumps({'Error': 'User exist but not have a private key'})

        else:
            return json.dumps({'Error': 'No user matching this unique code has been found'})

    @http.route('/User/user_public_key/<string:user_mobile_code_pin>', type='http', auth='public', cors='*')
    def send_user_private_key_notification(self, user_mobile_code_pin):
        user = http.request.env['res.users'].sudo().search([('user_mobile_code_pin', '=', user_mobile_code_pin)],
                                                           limit=1)
        if user and user.its_identity_ids:
            public_key = user.its_identity_ids[0].public_key
            user_public_key_parts = public_key.split(':')
            user_private_key_part1 = user_public_key_parts[0] if len(user_public_key_parts) > 0 else ""
            user_public_key_part2 = user_public_key_parts[1] if len(user_public_key_parts) > 1 else ""
            user_private_key_part1_int = int(user_private_key_part1)
            user_public_key_part2_int = int(user_public_key_part2)

            message = b"a"
            public_numbers = rsa.RSAPublicNumbers(
                user_private_key_part1_int,
                user_public_key_part2_int
            )
            print(public_numbers)

            public_key = public_numbers.public_key(default_backend())
            block_size = 245
            num_blocks = (len(message) + block_size - 1) // block_size
            ciphertext_blocks = []
            for i in range(num_blocks):
                block_start = i * block_size
                block_end = min((i + 1) * block_size, len(message))
                block = message[block_start:block_end]
                ciphertext_block = public_key.encrypt(block, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                          algorithm=hashes.SHA256(), label=None))
                ciphertext_blocks.append(ciphertext_block)
            ciphertext = b"".join(ciphertext_blocks)
            print(ciphertext)
            return "Message chiffré : {}".format(ciphertext.hex())

    @http.route('/User/generate_series', type='http', auth='public', cors='*')
    def generate_series(self):
        while True:
            series1 = sample(range(10), 2)
            series2 = sample(range(10), 2)
            series3 = sample(range(10), 2)

            if series1 != series2 and series1 != series3 and series2 != series3:
                break

        series1_str = ''.join(map(str, series1))
        series2_str = ''.join(map(str, series2))
        series3_str = ''.join(map(str, series3))

        data = {
            'series1': series1_str,
            'series2': series2_str,
            'series3': series3_str
        }

        message = 'Select number ended by 5 !'
        http.request.env['bus.bus'].sendone(
            'my_channel',
            json.dumps({'type': 'my_event', 'message': message})
        )

        with open('data.json', 'w') as f:
            json.dump(data, f)
        return http.request.make_response(json.dumps(data), headers={'Content-Type': 'application/json'})