#################################################################################
# File Name: res_user.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/08/2024    Add compnay name and address fields
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
from odoo import api, fields, models

class ResUsers(models.Model):
	_inherit = 'res.users'

	company_name = fields.Char(string='Company Name')

	company_address_str1 = fields.Char(string='Company Address Street1')
	company_address_str2 = fields.Char(string='Company Address Street2')
	company_address_city = fields.Char(string='Company Address City')
	company_address_state = fields.Char(string='Company Address State')
	company_address_cntry = fields.Char(string='Company Address Country')
	company_address_zip = fields.Char(string='Company Zip')
    
	customer_address_str1 = fields.Char(string='Customer Street1')
	customer_address_str2 = fields.Char(string='Customer Street2')
	customer_address_city = fields.Char(string='Customer City')
	customer_address_state = fields.Char(string='Customer State')
	customer_address_cntry = fields.Char(string='Customer Country')
	customer_address_zip = fields.Char(string='Customer Zip')

	@api.model
	def signup(self, values, token=None):
		""" signup a user, to either:
			- create a new user (no token), or
			- create a user for a partner (with token, but no user for partner), or
			- change the password of a user (with token, and existing user).
			:param values: a dictionary with field values that are written on user
			:param token: signup token (optional)
			:return: (dbname, login, password) for the signed up user
		"""
		
		if token:
			partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
			partner_user = partner.user_ids and partner.user_ids[0] or False
			if partner_user:
				values['phone'] = values.get('phone')
				values['company_name'] = values.get('company_name')
				values['company_address_str1'] = values.get('company_address_str1')
				values['company_address_str2'] = values.get('company_address_str2')
				values['company_address_city'] = values.get('company_address_city')
				values['company_address_state'] = values.get('company_address_state')
				values['company_address_cntry'] = values.get('company_address_cntry')
				values['company_address_zip'] = values.get('company_address_zip')
				values['customer_address_str1'] = values.get('customer_address_str1')
				values['customer_address_str2'] = values.get('customer_address_str2')
				values['customer_address_city'] = values.get('customer_address_city')
				values['customer_address_state'] = values.get('customer_address_state')
				values['customer_address_cntry'] = values.get('customer_address_cntry')
				values['customer_address_zip'] = values.get('customer_address_zip')

		else:	
			values['phone'] = values.get('phone')
			values['company_name'] = values.get('company_name')
			values['company_address_str1'] = values.get('company_address_str1')
			values['company_address_str2'] = values.get('company_address_str2')
			values['company_address_city'] = values.get('company_address_city')
			values['company_address_state'] = values.get('company_address_state')
			values['company_address_cntry'] = values.get('company_address_cntry')
			values['company_address_zip'] = values.get('company_address_zip')
			values['customer_address_str1'] = values.get('customer_address_str1')
			values['customer_address_str2'] = values.get('customer_address_str2')
			values['customer_address_city'] = values.get('customer_address_city')
			values['customer_address_state'] = values.get('customer_address_state')
			values['customer_address_cntry'] = values.get('customer_address_cntry')
			values['customer_address_zip'] = values.get('customer_address_zip')

		return super(ResUsers, self).signup(values, token)
		