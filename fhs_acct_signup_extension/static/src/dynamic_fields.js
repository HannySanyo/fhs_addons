odoo.define('auth_signup_extended.dynamic_fields', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var $ = require('jquery');

    publicWidget.registry.SignupForm = publicWidget.Widget.extend({
        selector: '#signup_form',
        events: {
            'change #company_address_cntry': '_onCountryChange',
        },

        _onCountryChange: function (event) {
            var countryId = $(event.currentTarget).val();
            var self = this;

            if (countryId) {
                this._rpc({
                    route: '/get_states',
                    params: { country_id: countryId },
                }).then(function (states) {
                    var $stateSelect = $('#company_address_state');
                    $stateSelect.empty().append('<option value="">Select State</option>');
                    states.forEach(function (state) {
                        $stateSelect.append('<option value="' + state.id + '">' + state.name + '</option>');
                    });
                });
            }
        },

        start: function () {
            this._rpc({
                route: '/get_countries',
                params: {},
            }).then(function (countries) {
                var $countrySelect = $('#company_address_cntry');
                countries.forEach(function (country) {
                    $countrySelect.append('<option value="' + country.id + '">' + country.name + '</option>');
                });
            });
        },
    });
});
