#################################################################################
# File Name: res_user.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/14/2024    Add address fields
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
from odoo import api, fields, models

class ResUsers(models.Model):
	_inherit = 'res.users'

	address_str1 = fields.Char(string='Street1')
	address_str2 = fields.Char(string='Street2')
	city = fields.Char(string='City')
	state_id = fields.Many2one('res.country.state', string='State')
	zip = fields.Char(string='Zip')

	@api.model
	def signup(self, values, token=None):
		""" 
        Signup a user, either:
        - create a new user (no token), or
        - create a user for a partner (with token), or
        - change the password of an existing user (with token).
        
        :param values: Dictionary with field values for the user
        :param token: Signup token (optional)
        :return: (dbname, login, password) for the signed-up user
        """
        
        # If a token is provided, retrieve the associated partner
		if token:
			partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
			partner_user = partner.user_ids and partner.user_ids[0] or False
            
			if partner_user:
				# Update values with partner's address details
				self._update_address_fields(values)

			else:
            	# For new user signup without a token
				self._update_address_fields(values)

		# Create the user with the updated values
		user = super(ResUsers, self).create(values)

		# Update the partner's address fields
		user.partner_id.write({
            'street': values.get('address_str1'),
            'street2': values.get('address_str2'),
            'city': values.get('city'),
            'state_id': values.get('state_id'),
            'zip': values.get('zip'),
        })

		return super(ResUsers, self).signup(values, token)

	def _update_address_fields(self, values):
		""" Helper method to update address fields in values dictionary. """
		values['phone'] = values.get('phone')
		values['address_str1'] = values.get('address_str1')
		values['address_str2'] = values.get('address_str2')
		values['city'] = values.get('city')
		values['state_id'] = values.get('state_id')
		values['zip'] = values.get('zip')
		