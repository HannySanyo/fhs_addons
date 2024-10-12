odoo.define('auth_signup_extended.dynamic_fields', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var $ = require('jquery');

    publicWidget.registry.SignupForm = publicWidget.Widget.extend({
        selector: '#signup_form',
        
        events: {
            'change #country': '_onCountryChange',
        },

        /**
         * Fetch and populate states when the selected country changes.
         */
        _onCountryChange: function (event) {
            var countryId = $(event.currentTarget).val();
            var self = this;

            if (countryId) {
                this._rpc({
                    route: '/get_states',
                    params: { country_id: countryId },
                }).then(function (states) {
                    var $stateSelect = $('#state');
                    $stateSelect.empty().append('<option value="">Select State</option>');

                    // Populate the states dropdown
                    states.forEach(function (state) {
                        $stateSelect.append('<option value="' + state.id + '">' + state.name + '</option>');
                    });
                });
            }
        },

        /**
         * Fetch and populate countries when the widget starts.
         */
        start: function () {
            var self = this;  // Reference to the current context

            this._rpc({
                route: '/get_countries',
                params: {},
            }).then(function (countries) {
                var $countrySelect = $('#country');

                // Populate the countries dropdown
                countries.forEach(function (country) {
                    $countrySelect.append('<option value="' + country.id + '">' + country.name + '</option>');
                });
            });
        },
    });
});
