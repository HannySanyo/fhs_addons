odoo.define('your_module.signup', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.SignupForm = publicWidget.Widget.extend({
        selector: '.o_signup_form',  // Adjust this selector to match your signup form
        events: {
            'input .company_name': '_onCompanyNameInput',
        },

        _onCompanyNameInput: function (event) {
            var companyName = $(event.currentTarget).val();
            if (companyName) {
                // Show company address fields
                this.$('.field-company_address').show();
                this.$('.field-customer_address').show();
            } else {
                // Hide company address fields
                this.$('.field-company_address').hide();
                this.$('.field-customer_address').hide();
            }
        },
    });
});
