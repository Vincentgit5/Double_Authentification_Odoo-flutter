from datetime import time

from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.portal.controllers.web import Home
from odoo.http import request


class CustomAuth(AuthSignupHome):
    @http.route('/auth_oauth/signin', type='http', auth='none')
    def web_login(self, *args, **kwargs):
        user = request.env.user
        if user and user.activate:
            time.sleep(120)
            return request.render('custom_auth.authentication_interrupted')
        # call the crypt function
        else:
            return super(CustomAuth, self).web_login(*args, **kwargs)


class CustomLogin(Home):
    @http.route('/web/login', type='http', auth='none')
    def do_login(self, **kw):
        custom_field = kw.get('custom_field')

        return super(CustomLogin, self).do_login(**kw)