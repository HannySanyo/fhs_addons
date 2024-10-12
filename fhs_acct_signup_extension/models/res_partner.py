#################################################################################
# File Name: res_partner.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/08/2024    Add address fields
#                    G. Sanyo    09/29/2024    Creation
#################################################################################

from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    address_str1 = fields.Char(string='Street1')
    address_str2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    zip = fields.Char(string='Zip')

    contractor_doc = fields.Binary(string='Contractor Doc', attachment=True)
    contractor_doc_filename = fields.Char(string='Contractor Doc Name')
    fiscal_pos_doc = fields.Binary(string='Fiscal Position Doc', attachment=True)
    fiscal_pos_doc_name = fields.Char(string='Fiscal Position Doc Name')

    @api.model
    def create_contact_record(self, vals):
        # Create the record
        record = super(ResPartnerInherit, self).create(vals)

        # Set address fields
        if vals.get('address_str1'):
            record.street = vals.get('address_str1')
            record.street2 = vals.get('address_str2')
            record.city = vals.get('city')
            record.state_id = vals.get('state_id')
            record.zip = vals.get('zip')
            record.country_id = vals.get('country_id')

        # Create attachments if the binary fields have data
        if vals.get('fiscal_pos_doc'):
            self.env['ir.attachment'].create({
                'name': vals.get('fiscal_pos_doc_name'),
                'type': 'binary',
                'datas': vals.get('fiscal_pos_doc'),
                'res_model': self._name,
                'res_id': record.id,
            })

        if vals.get('contractor_doc'):
            self.env['ir.attachment'].create({
                'name': vals.get('contractor_doc_filename'),
                'type': 'binary',
                'datas': vals.get('contractor_doc'),
                'res_model': self._name,
                'res_id': record.id,
            })

        return record
