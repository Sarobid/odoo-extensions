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
            this.rmaSeleted = null;
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
                if (rma.length > 0) {
                    self.rmaSeleted = rma[0]   
                }
                self._showDetailsVehicleRma();
                w3_open()
                self._showTaskVehicleRma();
            });
        },
        _render_button_close_details : function () { 
            const self = this;
            this.$el.find('#close-details-vehicle').on('click', function (e) {
                w3_close()
            }); 
        },
        _showDetailsVehicleRma : function () {
            if(this.rmaSeleted){
                console.log(core.qweb)
                insertDetailsVehicleInHtml(core.qweb,this.rmaSeleted)
            }
        },
        _showTaskVehicleRma : function () {
            if(this.rmaSeleted){
                getAllTaskVehicleRma(this,this.rmaSeleted.rma_id,function (data) {
                    console.log("task rma",data)
                    insertTacheVehicleInHtml(core.qweb,data)
                })
            }
        }

    });
    
    core.action_registry.add('smart_ui_tools.vehicle.rma', HomePage);
    return HomePage;
});