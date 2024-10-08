#################################################################################
# File Name: main.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/08/2024    Add company name and address fields
#                    G. Sanyo    10/03/2024    Add attachments for contractor doc
#                                              and fiscal position doc
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
import base64
from odoo import _
from odoo import http
from odoo.http import request,route
from odoo.exceptions import UserError
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
    
class AuthSignupHomeInherit(AuthSignupHome, http.Controller):

    @http.route('/get_countries', type='json', auth='public')
    def get_countries(self):
        countries = request.env['res.country'].search([])
        return [{'id': country.id, 'name': country.name} for country in countries]

    @http.route('/get_states', type='json', auth='public')
    def get_states(self, country_id):
        states = request.env['res.country.state'].search([('country_id', '=', country_id)])
        return [{'id': state.id, 'name': state.name} for state in states]

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in (
            'login',
            'name',
            'company_name',
            'company_address_str1',
            'company_address_str2',
            'company_address_city',
            'company_address_state',
            'company_address_cntry',
            'company_address_zip',
            'customer_address_str1',
            'customer_address_str2',
            'customer_address_city',
            'customer_address_state',
            'customer_address_cntry',
            'customer_address_zip',
            'password',
            'phone',
            'fiscal_pos_doc',
            'fiscal_pos_doc_name',
            'contractor_doc',
            'contractor_doc_filename'
        ) }

        if not values:
            raise UserError(_("The form was not properly filled in."))
        
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        
        if values.get('company_name'):
            values.update({
                'company_name': values.get('company_name'),
                'company_address_str1': values.get('company_address_str1'),
                'company_address_str2': values.get('company_address_str2'),
                'company_address_city': values.get('company_address_city'),
                'company_address_state': values.get('company_address_state'),
                'company_address_zip': values.get('company_address_zip'),
                'company_address_cntry': values.get('company_address_cntry'),
                'street': values.get('company_address_str1'),
                'street2': values.get('company_address_str2'),
                'city': values.get('company_address_city'),
                'state_id': values.get('company_address_state'),
                'zip': values.get('company_address_zip'),
                'country_id': values.get('company_address_cntry'),
            })
        else:
            values.update({
                'customer_address_str1': values.get('customer_address_str1'),
                'customer_address_str2': values.get('customer_address_str2'),
                'customer_address_city': values.get('customer_address_city'),
                'customer_address_state': values.get('customer_address_state'),
                'customer_address_zip': values.get('customer_address_zip'),
                'customer_address_cntry': values.get('customer_address_cntry'),
                'street': values.get('customer_address_str1'),
                'street2': values.get('customer_address_str2'),
                'city': values.get('customer_address_city'),
                'state_id': values.get('customer_address_state'),
                'zip': values.get('customer_address_zip'),
                'country_id': values.get('customer_address_cntry'),
            })

        if values.get('fiscal_pos_doc_name'):
            datas = base64.b64encode(values.get('fiscal_pos_doc').read())
            filename = values.get('fiscal_pos_doc').filename
            values.update({
                'fiscal_pos_doc': datas,
                'fiscal_pos_doc_name': filename,
                'x_studio_fiscal_doc': datas,
                'x_studio_fiscal_doc_filename': filename
            })

        if values.get('contractor_doc'):
            datas = base64.b64encode(values.get('contractor_doc').read())
            filename = values.get('contractor_doc').filename
            values.update({
                'contractor_doc': datas,
                'contractor_doc_filename': filename,
                'x_studio_contractor_doc': datas,
                'x_studio_contractor_doc_filename': filename
            })

        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def get_auth_signup_qcontext(self):
        SIGN_UP_REQUEST_PARAMS.update({
            'phone',
            'company_name',
            'company_address_str1',
            'company_address_str2',
            'company_address_city',
            'company_address_state',
            'company_address_cntry',
            'company_address_zip',
            'customer_address_str1',
            'customer_address_str2',
            'customer_address_city',
            'customer_address_state',
            'customer_address_cntry',
            'customer_address_zip',
            'fiscal_pos_doc',
            'fiscal_pos_doc_name',
            'contractor_doc',
            'contractor_doc_filename'
        })

        return super().get_auth_signup_qcontext()