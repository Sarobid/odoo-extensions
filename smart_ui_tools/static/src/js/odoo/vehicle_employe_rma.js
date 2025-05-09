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
            // console.log("user id",session.uid)
            return Promise.all([]);
        },
        start: function () {
            const self = this;
            console.log(self.dataVehicle)
            const templateHtml = core.qweb.render('PageMainVehicleRma', {
                // dataVehicle: self.dataVehicle
            });
            this.$el.html(templateHtml);
            self._showListVehicleRma()
            self._render_button_details();
            self._render_button_close_details();
            self._render_start_button_task();
            self._render_end_button_task();
            return this._super.apply(this, arguments);
        },
        _render_button_details : function () {
            const self = this;
            // this.$el.find('.vehicle-card').on('click', function (e) {
            this.$el.off('click', '.vehicle-card'); // Nettoie les anciens écouteurs s'il y en a
            this.$el.on('click', '.vehicle-card', function (e) {
                    e.preventDefault();
                const recordId = $(this).data('id');
                // console.log("RMA employee, ID =", recordId);
                let rma = getDetailsRma(self.dataVehicle,recordId)
                // console.log("rma",rma)
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
        _render_start_button_task : function (){
            const self = this;
            this.$el.off('click', '.start-button-task'); // Nettoie les anciens écouteurs s'il y en a
            this.$el.on('click', '.start-button-task', function (e) {
                e.preventDefault();
                const recordId = $(this).data('id');
                // alert("start");
                 apiStart(self,recordId,function () {
                    self._showTaskVehicleRma();
                 })
            });
        },
        _render_end_button_task : function (){
            const self = this;
            this.$el.off('click', '.end-button-task'); // Nettoie les anciens écouteurs s'il y en a
            this.$el.on('click', '.end-button-task', function (e) {
                e.preventDefault();
                const recordId = $(this).data('id');
                // alert("start");
                apiEnd(self,recordId,function () {
                    self._showTaskVehicleRma();
                })
            });
        },
        _showListVehicleRma : function () {
            const self = this;
            getAllVehicleRmaMecano(this,session.uid,function (data){
                self.dataVehicle = data
                insertListVehicleInHtml(core.qweb,self.dataVehicle)
            }) 
        },
        _showDetailsVehicleRma : function () {
            if(this.rmaSeleted){
                // console.log(core.qweb)
                insertDetailsVehicleInHtml(core.qweb,this.rmaSeleted)
            }
        },
        _showTaskVehicleRma : function () {
            const self = this;
            if(this.rmaSeleted){
                getAllTaskVehicleRma(this,this.rmaSeleted.rma_id,function (data) {
                    // console.log("task rma",data)
                    let dataGroup = taskVehicleGroupByRma(data,session.uid)
                    let dataGroupSortByRepairId = taskVehicleRmaSortByRepairId(dataGroup);
                    let taskAssigne = getTaskAssigne(dataGroupSortByRepairId);
                    let noEndTask =  getTaskNotEnd(taskAssigne)
                    let noStartTask =  getTaskNotStart(taskAssigne)
                    showTaskAssigneAndNo(taskAssigne.length,dataGroupSortByRepairId.length - taskAssigne.length,noStartTask.length,
                        noEndTask.length
                    )
                    insertTacheVehicleInHtml(core.qweb,dataGroupSortByRepairId);
                    if(noEndTask.length === 0 && noStartTask.length === 0){
                        self._showListVehicleRma();
                    }
                    
                })
            }
        }

    });
    
    core.action_registry.add('smart_ui_tools.vehicle.rma', HomePage);
    return HomePage;
});