/** @odoo-module **/

/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { Order } from "@point_of_sale/app/store/models";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { SignaturePopupWidget } from "@pos_signature/app/popups/signature_popup/signature_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { WaitingForSignature } from "@pos_signature/app/popups/waiting_for_signature_popup/waiting_for_signature_popup";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        if(options.json && options.json.signature){
            this.signature = options.json.signature;
            this.is_signature_draw = options.json.is_signature_draw;
        }else{
            this.signature = '';
        }
        this.clicking = false;
        this.mouse = { x: 0, y: 0 };
        this.canvas;
        this.ctx;
        super.setup(...arguments);
    },
    export_as_JSON() {
        var self = this;
        var json = super.export_as_JSON();
        if (self.pos.get_order() != null){
            json.signature = self.pos.get_order().signature;
            json.is_signature_draw = self.pos.get_order().is_signature_draw;
        }
        return json;
    },


    init_from_JSON(json) {
        var self = this;
        super.init_from_JSON(...arguments);
        if (self.pos.get_order() != null ){
            this.signature = json.signature;
            this.is_signature_draw = json.is_signature_draw;
        }
    },

    export_for_printing() {
        return{
            ...super.export_for_printing(...arguments),
            signature: this.signature,
            is_signature_draw: this.is_signature_draw
        }
    },

})

patch(OrderReceipt.prototype, {
    async setup() {
        super.setup(...arguments);
        var self = this;
        if (self.props.data.signature == '') {
            $("#customer_signature_table").hide();
        }
        else {
            var signature = "data:image/png;base64," + await self.props.data.signature;
            var image = new Image();
            image.src = signature;
        }
    }
})

patch(PaymentScreen.prototype, {

    setup(){
        super.setup(...arguments);
        this.customerDisplay = useService("customer_display");
    },

    async add_signature(event) {
        const current_order = this.pos.get_order();
        if(this.pos.config.add_signature_from && this.pos.config.add_signature_from === 'cutomer_screen' && this.pos.config.iface_customer_facing_display_local){
            if(this.customerDisplay.isPopupWindowLastStatusOpen()){
                this.popup.add(WaitingForSignature,{})
                if(!current_order.signature != '' || !current_order.is_signature_draw)
                    this.customerDisplay?.update({ enableSign: true });
            }
            else{
                this.popup.add(ErrorPopup,{
                    title: _t("Customer screen is not opened !"),
                    body: _t("Please open the customer screen to take the customer's signature.")
                })
            }
        }
        else{
            await this.popup.add(SignaturePopupWidget, {})
        }
    },

    async validateOrder(isForceValidate) {
        if (this.pos.config.enable_pos_signature && this.pos.config.set_signature_mandatory) {
            if (this.pos.get_order().signature === '' || this.pos.get_order().is_signature_draw === undefined) {
                this.pos.get_order().signature = '';
                this.pos.get_order().canvas = '';
                this.pos.get_order().ctx = '';
                this.pos.get_order().mouse = { x: 0, y: 0 };
                await this.popup.add(ErrorPopup, {
                    title: _t("Signature Required.."),
                    body: _t("Please Add Signature"),
                });
            } else {
                super.validateOrder(...arguments);
            }
        } else {
            super.validateOrder(...arguments);
        }
    }
});


