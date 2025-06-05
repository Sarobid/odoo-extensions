/** @odoo-module **/
odoo.define('viseo_pos.list.piece.mecano', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var session = require('web.session');
    var HomePage = AbstractAction.extend({
        cssLibs: [],
        init : function (){
            this._super.apply(this, arguments);
            this.dataPieceMecano = [];
        },
        willStart : function(){
            const self = this;
            return Promise.all([]);
        },
        start: function () {
            const self = this;
            const templateHtml = core.qweb.render('PageMainListePieceMecano', {});
            this.$el.html(templateHtml);
            self._show_listPieceMecano();
            self._render_valid_button();
            self._render_denied_button();
            return this._super.apply(this, arguments);
        },
        _show_listPieceMecano: function () {
            const self = this;
            pieceMecanoService.getAllListePieceMecano(self, function (data) {
                self.dataPieceMecano = data;
                // console.log("Liste des pièces mécano", self.dataPieceMecano);
                pieceMecanoService.insertListePieceMecanoInHtml(core.qweb, data);
            });
        },
        _render_denied_button : function (){
            const self = this;
            this._render_click_button_check_piece(function (piece) {
                pieceMecanoService.deniedPieceMecano(self, piece.stock_move_line_id[0], function (data) {
                    // console.log("Refus réussi", data);
                    pieceMecanoService.showMessageSucces('message-denied-success');
                    // self._show_listPieceMecano();
                });
            }, 'denied-button');
        },
        _render_valid_button : function (){
            const self = this;
            this._render_click_button_check_piece(function (piece) {
                pieceMecanoService.validPieceMecano(self, piece.stock_move_line_id[0], function (data) {
                    // console.log("Validation réussie", data);
                    pieceMecanoService.showMessageSucces('message-valid-success');
                    // self._show_listPieceMecano();
                });
            }, 'valid-button');
        },
        _render_click_button_check_piece : function (functionTraite, buttonClass){
            console.log("Render click button check piece", buttonClass);
            const self = this;
            this.$el.off('click', '.' + buttonClass);
            this.$el.on('click', '.'+ buttonClass, function (e) {
                e.preventDefault();
                const recordId = $(this).data('id');
                // alert("start");
                let pieces = pieceMecanoService.getPiecesSelected(self.dataPieceMecano,recordId);
                console.log("Selected piece", pieces);
                if (pieces.length > 0) {
                    functionTraite(pieces[0]);
                }
            });
        }
    });
    core.action_registry.add('viseo_pos.list.piece.mecano', HomePage);
    return HomePage;
});