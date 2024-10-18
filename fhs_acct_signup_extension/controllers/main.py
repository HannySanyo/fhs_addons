import base64
from odoo import _
from odoo import http
from odoo.http import request, route
from odoo.exceptions import UserError
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

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

        # Update address fields
        if values.get('address_str1'):
            values.update({
                'street': values.get('address_str1'),
                'street2': values.get('address_str2'),
                'city': values.get('city'),
                'state_id': values.get('state_id'),
                'zip': values.get('zip'),
            })

        # Handle fiscal document upload
        if values.get('fiscal_pos_doc'):
            if hasattr(values['fiscal_pos_doc'], 'read'):
                datas = base64.b64encode(values['fiscal_pos_doc'].read()).decode('utf-8')
                filename = values['fiscal_pos_doc'].filename
                values.update({
                    'x_studio_fiscal_doc': datas,
                    'x_studio_fiscal_doc_filename': filename
                })
            else:
                raise UserError(_("Invalid fiscal position document uploaded."))

        # Handle contractor document upload
        if values.get('contractor_doc'):
            if hasattr(values['contractor_doc'], 'read'):
                datas = base64.b64encode(values['contractor_doc'].read()).decode('utf-8')
                filename = values['contractor_doc'].filename
                values.update({
                    'x_studio_contractor_doc': datas,
                    'x_studio_contractor_doc_filename': filename
                })
            else:
                raise UserError(_("Invalid contractor document uploaded."))

        # Set language
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.env.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang

        # Perform signup
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def get_auth_signup_qcontext(self):
        qcontext = super(AuthSignupHomeInherit, self).get_auth_signup_qcontext()

        # Hard-coded United States for country for now
        unitedstates = request.env['res.country'].sudo().search([('code', '=', 'US')], limit=1)

        # Check if country is found and use its ID
        if unitedstates:
            country_id = unitedstates.id
            qcontext['states'] = request.env['res.country.state'].sudo().search([('country_id', '=', country_id)])
        else:
            qcontext['states'] = request.env['res.country.state'].sudo().browse([])  # No states if country not found

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