/** @odoo-module **/
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { onMounted, useState } from "@odoo/owl";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { memoize } from "@web/core/utils/functions";
import { renderToString } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";


const getProductImage = memoize(function getProductImage(productId, writeDate) {
    return new Promise(function (resolve, reject) {
        const img = new Image();
        img.addEventListener("load", () => {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            canvas.height = img.height;
            canvas.width = img.width;
            ctx.drawImage(img, 0, 0);
            resolve(canvas.toDataURL("image/jpeg"));
        });
        img.addEventListener("error", reject);
        img.src = `/web/image?model=product.product&field=image_128&id=${productId}&unique=${writeDate}`;
    });
});

patch(PosStore.prototype, {

    async customerSignatureHTML(){
        const order = this.get_order();
        const orderLines = order.get_orderlines();

        const productImages = Object.fromEntries(
            await Promise.all(
                orderLines.map(async ({ product }) => [
                    product.id,
                    await getProductImage(product.id, product.writeDate),
                ])
            )
        );

        return renderToString("point_of_sale.CustomerSignatureScreen", {
            pos: this,
            origin: window.location.origin,
            formatCurrency: this.env.utils.formatCurrency,
            order,
            productImages
        });
    }
});

export class WaitingForSignature extends AbstractAwaitablePopup {
    static template = "pos_signature.WaitingForSignature";
    async setup() {
        super.setup();
        this.pos = usePos();
        this.currentOrder = this.pos.get_order();
        this.customerDisplay = useService("customer_display");
        this.state = useState({
            'is_signed': false,
        })
        onMounted(this.onMounted)
    }

    waitForSignature(){
        var self = this;
        return new Promise((resolve)=>{
            const checkSignature = ()=>{
                if(!self.currentOrder.signature=='' && self.currentOrder.is_signature_draw){
                    resolve(true)
                }
                else{
                    setTimeout(checkSignature,100)
                }
            };
            checkSignature();
        })
    }

    async onMounted() {
        if (this.currentOrder.signature && this.currentOrder.is_signature_draw) {
            this.state.is_signed = true;
            let data = "data:image/png;base64," + this.currentOrder.signature;
            let newImg = new Image();
            newImg.src = data;
            newImg.style.width = '100%';
            newImg.style.height = '200px';
            
            await new Promise((resolve) => {
                if(newImg){
                    newImg.onload = resolve;
                }
            })   
            setTimeout(()=>{
                let $sign_box = $('.signature-box');
                $sign_box.append(newImg);
            },120)
            
            return;
        }
        await this.waitForSignature().then(value=>{
            this.customerDisplay.update();
            this.confirm();
        })
    }

    async retake(){
        this.state.is_signed = false;
        this.customerDisplay?.update({ enableSign: true });
        this.currentOrder.is_signature_draw=false;
        await this.waitForSignature().then(value=>{
            this.confirm(); 
        })
    }
    confirm(){
        this.customerDisplay.update();
        
        super.confirm();
    }

    cancel(){
        if(this.currentOrder.signature!=''){
            this.currentOrder.is_signature_draw=true;
        }
        super.cancel();
        this.customerDisplay.update();
    }
    delete_sign(){
        this.currentOrder.signature='';
        this.currentOrder.is_signature_draw=false;
        this.cancel();
    }
}