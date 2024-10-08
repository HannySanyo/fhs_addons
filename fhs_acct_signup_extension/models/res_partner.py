from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    company_name = fields.Char(string='Company Name')
    company_address_str1 = fields.Char(string='Company Address Street1')
    company_address_str2 = fields.Char(string='Company Address Street2')
    company_address_city = fields.Char(string='Company Address City')
    company_address_state = fields.Many2one('res.country.state', string='Company Address State')
    company_address_cntry = fields.Many2one('res.country', string='Company Address Country')
    company_address_zip = fields.Char(string='Company Zip')

    customer_address_str1 = fields.Char(string='Customer Street1')
    customer_address_str2 = fields.Char(string='Customer Street2')
    customer_address_city = fields.Char(string='Customer City')
    customer_address_state = fields.Many2one('res.country.state', string='Customer Address State')
    customer_address_cntry = fields.Many2one('res.country', string='Customer Address Country')
    customer_address_zip = fields.Char(string='Customer Zip')

    contractor_doc = fields.Binary(string='Contractor Doc', attachment=True)
    contractor_doc_filename = fields.Char(string='Contractor Doc Name')
    fiscal_pos_doc = fields.Binary(string='Fiscal Position Doc', attachment=True)
    fiscal_pos_doc_name = fields.Char(string='Fiscal Position Doc Name')

    @api.model
    def create_contact_record(self, vals):
        # Create the record
        record = super(ResPartnerInherit, self).create(vals)

        # Set address fields based on whether it's a company or customer
        if vals.get('company_name'):
            record.street = vals.get('company_address_str1')
            record.street2 = vals.get('company_address_str2')
            record.city = vals.get('company_address_city')
            record.state_id = vals.get('company_address_state')
            record.zip = vals.get('company_address_zip')
            record.country_id = vals.get('company_address_cntry')
        else:
            record.street = vals.get('customer_address_str1')
            record.street2 = vals.get('customer_address_str2')
            record.city = vals.get('customer_address_city')
            record.state_id = vals.get('customer_address_state')
            record.zip = vals.get('customer_address_zip')
            record.country_id = vals.get('customer_address_cntry')

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
