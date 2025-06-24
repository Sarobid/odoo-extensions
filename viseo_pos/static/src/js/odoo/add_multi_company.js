odoo.define('viseo_pos.user_menu_multi_company', function (require) {
    "use strict";

    var UserMenu = require('web.UserMenu');
    var session = require('web.session');

    UserMenu.include({
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                //  console.log('UserMenu started');
                //  console.log('session', session);
                if (window.is_mecano) {
                    var allowed_company_ids = session.companies_currency_id
                    //  console.log('allowed_company_ids', allowed_company_ids, session.user_context.allowed_company_ids);
                    var allowed_company_ids_array= Object.keys(allowed_company_ids).map(key => Number(key)) 
                    if (allowed_company_ids && session.user_context.allowed_company_ids.length != allowed_company_ids_array.length) {
                        session.user_context.allowed_company_ids = allowed_company_ids_array
                        //  console.log('Toutes les sociétés sont sélectionnées');
                        // window.location.reload();
                    }
                }
            });
        },
    });
});
