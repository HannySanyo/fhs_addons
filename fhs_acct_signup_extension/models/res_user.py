#################################################################################
# File Name: res_user.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/08/2024    Add address fields
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
from odoo import api, fields, models

class ResUsers(models.Model):
	_inherit = 'res.users'
    
	address_str1 = fields.Char(string='Street1')
	address_str2 = fields.Char(string='Street2')
	address_city = fields.Char(string='City')
	address_state = fields.Char(string='State')
	address_cntry = fields.Char(string='Country')
	address_zip = fields.Char(string='Zip')

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
				values['address_str1'] = values.get('address_str1')
				values['address_str2'] = values.get('address_str2')
				values['address_city'] = values.get('address_city')
				values['address_state'] = values.get('address_state')
				values['address_cntry'] = values.get('address_cntry')
				values['address_zip'] = values.get('address_zip')

		else:	
			values['phone'] = values.get('phone')
			values['address_str1'] = values.get('address_str1')
			values['address_str2'] = values.get('address_str2')
			values['address_city'] = values.get('address_city')
			values['address_state'] = values.get('address_state')
			values['address_cntry'] = values.get('address_cntry')
			values['address_zip'] = values.get('address_zip')

		return super(ResUsers, self).signup(values, token)
		