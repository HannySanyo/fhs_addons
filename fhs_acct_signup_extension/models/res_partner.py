#################################################################################
# File Name: res_partner.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/08/2024    Add company name and address fields
#                    G. Sanyo    10/03/2024    Add attachments for contractor doc
#                                              and fiscal position doc
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

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

    contractor_doc = fields.Binary(string='Contractor Doc', attachment=True)
    contractor_doc_filename = fields.Char(string='Contractor Doc Name')
    fiscal_pos_doc = fields.Binary(string='Fiscal Position Doc', attachment=True)
    fiscal_pos_doc_name = fields.Char(string='Fiscal Position Doc Name')


    @api.model
    def create_attachment_record(self, vals):
        # Create the record
        record = super(ResPartnerInherit, self).create(vals)

        # Create an fiscal_pos_doc if the binary field has data
        if vals.get('fiscal_pos_doc'):

            self.env['ir.attachment'].create_attachment_record({
                'name': vals.get('fiscal_pos_doc_name'),
                'type': 'binary',
                'datas': vals.get('fiscal_pos_doc'),
                'res_model': self._name,
                'res_id': record.id,
            })

        # Create an attachment if the binary field has data
        if vals.get('contractor_doc'):

            self.env['ir.attachment'].create_attachment_record({
                'name': vals.get('contractor_doc'),
                'type': 'binary',
                'datas': vals.get('contractor_doc'),
                'res_model': self._name,
                'res_id': record.id,
            })
            
        return record

