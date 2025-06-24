# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect

class ViseoPosController(http.Controller):
    @http.route('/token_login/login', type='http', auth='public', csrf=False)
    def login_via_token(self, token=None,dbname=None):
        if not token and not dbname:
            return redirect('/web/login')
        user = request.env['res.users'].sudo().search([('token_mobile', '=', token)], limit=1)
        if not user:
            return redirect('/web/login')
        request.session.authenticate(dbname, user.login, token)
        print("Token cleared for user:", user.login)
        return redirect('/web')