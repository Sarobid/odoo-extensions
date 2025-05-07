/** @odoo-module **/
odoo.define('smart_ui_tools.vehicle.rma', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var session = require('web.session');
    var HomePage = AbstractAction.extend({
        cssLibs: [],
        init : function (){
            //INitialisation des variable///
            this._super.apply(this, arguments);
            this.dataVehicle = []
        },
        willStart : function(){
            const self = this;
            console.log("user id",session.uid)
            return Promise.all([getAllVehicleRmaMecano(self,session.uid,function (data){
                self.dataVehicle = data
            })]);
        },
        start: function () {
            const self = this;
            console.log(self.dataVehicle)
            const templateHtml = core.qweb.render('PageListeVehicleRma', {
                dataVehicle: self.dataVehicle
            });
            this.$el.html(templateHtml);
            self._render_button_details();
            self._render_button_close_details();
            return this._super.apply(this, arguments);
        },
        _render_button_details : function () {
            const self = this;
            this.$el.find('.vehicle-card').on('click', function (e) {
                const recordId = $(this).data('id');
                console.log("RMA employee, ID =", recordId);
                let rma = getDetailsRma(self.dataVehicle,recordId)
                console.log("rma",rma)
                insertDetailsVehicleInHtml(core.qweb,rma[0])
                w3_open()
            });
        },
        _render_button_close_details : function () { 
            const self = this;
            this.$el.find('#close-details-vehicle').on('click', function (e) {
                w3_close()
            }); 
        }

    });
    
    core.action_registry.add('smart_ui_tools.vehicle.rma', HomePage);
    return HomePage;
});