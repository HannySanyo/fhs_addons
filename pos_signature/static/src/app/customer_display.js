/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import {LocalDisplay } from "@point_of_sale/app/customer_display/customer_display_service";

patch(LocalDisplay.prototype,{
    setup(){
        super.setup(...arguments);
    },


    async update({ refreshResources = false, closeUI = false , enableSign=false} = {}){
        if(this.popupWindow && this.isPopupWindowLastStatusOpen()){
            setTimeout(()=>{
                if(enableSign){
                    this.getSignature(this.popupWindow.document);
                }
            },500)
        }
        await super.update (...arguments)
    },

    async getSignature(){
        var self = this;
        const { body: displayBody, head: displayHead } = this.popupWindow.document;
        const container = document.createElement("div");
        container.innerHTML = await this.pos.customerSignatureHTML();
        if (!container.innerHTML || container.innerHTML === "undefined") {
            displayBody.textContent = "";
            return;
        }

        if (displayHead.innerHTML.trim().length == 0) {
            displayHead.textContent = "";
            displayHead.appendChild(container.querySelector(".resources"));
            // The scripts must be evaluated because adding an element containing
            // a script block doesn't make it evaluated.
            const scriptContent = displayHead.querySelector(
                "script#old_browser_fix_auto_scroll"
            ).innerHTML;
            this.popupWindow.eval(scriptContent);
        }

        displayBody.textContent = "";
        displayBody.appendChild(container.querySelector(".pos-customer_facing_display"));

        const canvas = displayBody.getElementsByTagName('canvas')[0];
        



        // const canvas = document.getElementById('signature-pad');
        const ctx = canvas.getContext('2d');
        
        // Set initial styles for drawing
        ctx.lineWidth = 1;
        ctx.lineCap = 'round'; // Round strokes for smoother lines
        ctx.strokeStyle = '#000';
        ctx.lineJoin = 'round';
        let drawing = false;
        let signature_done = false;
        let lastX = 0;
        let lastY = 0;
        
        // Function to get the accurate mouse/touch position relative to the canvas
        function getPosition(event) {
            const rect = canvas.getBoundingClientRect(); // Get canvas position and size
        
            // Adjust the coordinates based on the canvas's scale
            const scaleX = canvas.width / rect.width;   // Horizontal scale
            const scaleY = canvas.height / rect.height; // Vertical scale
        
            let x, y;
            if (event.type.includes('touch')) {
                const touch = event.touches[0]; // Handle the first touch point
                x = (touch.clientX - rect.left) * scaleX; // Scale touch position
                y = (touch.clientY - rect.top) * scaleY;
            } else {
                x = (event.clientX - rect.left) * scaleX; // Scale mouse position
                y = (event.clientY - rect.top) * scaleY;
            }
        
            return { x, y };
        }
        
        // Function to start drawing
        function startDrawing(event) {
            drawing = true;
            const { x, y } = getPosition(event);
            [lastX, lastY] = [x, y];
        }
        
        // Function to stop drawing
        function stopDrawing() {
            drawing = false;
            ctx.beginPath(); // Reset the path to avoid connecting lines between strokes
        }
        
        // Function to draw on the canvas
        function draw(event) {
            if (!drawing) return;
        
            const { x, y } = getPosition(event);
            signature_done = true;
            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath(); // Reset the path
            ctx.moveTo(x, y); // Move to the current position for the next line segment
        
            [lastX, lastY] = [x, y]; // Update the last coordinates
        }
        
        // Event listeners for mouse events
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing);
        
        // Event listeners for touch events (mobile devices)
        canvas.addEventListener('touchstart', startDrawing);
        canvas.addEventListener('touchmove', draw);
        canvas.addEventListener('touchend', stopDrawing);
        
        // Prevent scrolling while drawing on touch devices
        canvas.addEventListener('touchmove', (event) => event.preventDefault(), { passive: false });
        
        displayBody.querySelector('.submit-signature').addEventListener('click',function(){
            const current_order = self.pos.get_order();
            if(signature_done){
                current_order.signature = canvas.toDataURL('image/png').replace('data:image/png;base64,', "");
                current_order.is_signature_draw = true;
            }
        })

        displayBody.querySelector('.clear-button').addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            signature_done = false;
        });


        setTimeout(() => {
            this.popupWindow.fixScrollingIfNecessary();
        }, 0);
    }
})