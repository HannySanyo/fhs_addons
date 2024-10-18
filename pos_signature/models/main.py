# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    signature = fields.Binary(string='Customer Signature', readonly=True)

    @api.model
    def _order_fields(self, ui_order):
        fields_return = super(PosOrder, self)._order_fields(ui_order)
        fields_return.update({'signature': ui_order.get('signature', '')})
        return fields_return
    
    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result['signature'] = order.signature
        return result
    
class PosConfig(models.Model):
    _inherit = "pos.config"

    enable_pos_signature = fields.Boolean("Enable POS Signature")
    enable_signature_in_invoice = fields.Boolean("Show Signature in Invoice")
    set_signature_mandatory = fields.Boolean("Set Signature as Mandatory")
    add_signature_from = fields.Selection([('payment_screen', 'Payment Screen'), ('cutomer_screen', 'Customer Screen')], string='Add signature from', readonly=False, default='payment_screen')

    def check_for_invoice(self, config_id):
        record = self.search([('id', '=', config_id)])
        for rec in record:
            if(rec.enable_pos_signature == True and rec.enable_signature_in_invoice == True):
                return True
            else:
                return False


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_pos_signature = fields.Boolean(related="pos_config_id.enable_pos_signature", readonly=False)
    is_signature_in_invoice = fields.Boolean(related="pos_config_id.enable_signature_in_invoice", readonly=False)
    is_signature_mandatory= fields.Boolean(related="pos_config_id.set_signature_mandatory", readonly=False)
    pos_add_signature_from = fields.Selection(related='pos_config_id.add_signature_from', readonly=False)

