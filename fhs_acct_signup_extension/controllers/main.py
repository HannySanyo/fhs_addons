#################################################################################
# File Name: main.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/14/2024    Add address fields
#                    G. Sanyo    10/03/2024    Add attachments for contractor doc
#                                              and fiscal position doc
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
import base64
from odoo import _
from odoo import http
from odoo.http import request, route
from odoo.exceptions import UserError
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import SUPERUSER_ID

class AuthSignupHomeInherit(AuthSignupHome):

    def do_signup(self, qcontext):

        values = {key: qcontext.get(key) for key in (
            'login',
            'name',
            'address_str1',
            'address_str2',
            'city',
            'state_id',
            'zip',
            'password',
            'phone',
            'fiscal_pos_doc',
            'fiscal_pos_doc_name',
            'contractor_doc',
            'contractor_doc_filename'
        )}

        if not values:
            raise UserError(_("The form was not properly filled in."))
        
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        
        if values.get('address_str1'):
            values.update({
                'street': values.get('address_str1'),
                'street2': values.get('address_str2'),
                'city': values.get('city'),
                'state_id': values.get('state_id'),
                'zip': values.get('zip'),
            })

        if values.get('fiscal_pos_doc_name'):
            datas = base64.b64encode(values.get('fiscal_pos_doc').read())
            filename = values.get('fiscal_pos_doc').filename
            values.update({
                'x_studio_fiscal_doc': datas,
                'x_studio_fiscal_doc_filename': filename
            })

        if values.get('contractor_doc'):
            datas = base64.b64encode(values.get('contractor_doc').read())
            filename = values.get('contractor_doc').filename
            values.update({
                'x_studio_contractor_doc': datas,
                'x_studio_contractor_doc_filename': filename
            })

        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.env.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
            
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def get_auth_signup_qcontext(self):
        qcontext = super(AuthSignupHomeInherit, self).get_auth_signup_qcontext()

        qcontext['states'] = request.env["res.country.state"].sudo().search([])

        SIGN_UP_REQUEST_PARAMS.update({
            'phone',
            'address_str1',
            'address_str2',
            'city',
            'state_id',
            'zip',
            'fiscal_pos_doc',
            'fiscal_pos_doc_name',
            'contractor_doc',
            'contractor_doc_filename'
        })
        
        return qcontext