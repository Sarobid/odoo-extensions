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
            this.stock_piking_id = null;
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
            self._render_valid_all_button();
            self._render_valid_button();
            self._render_denied_button();
            return this._super.apply(this, arguments);
        },
        _show_listPieceMecano: function () {
            const self = this;
            pieceMecanoService.getAllListePieceMecano(self, function (data) {
                self.dataPieceMecano = data;
                if (self.dataPieceMecano.length > 0) {
                    self.stock_piking_id = self.dataPieceMecano[0].picking_sav[0];
                    pieceMecanoService.verificationDisponibilite(self,self.stock_piking_id,session.company_id, function (data) {
                        pieceMecanoService.getAllListePieceMecano(self, function (data) {
                            self.dataPieceMecano = pieceMecanoService.get_piece_reserverd_availability_is_valid(data);
                            console.log("Liste des pièces mécano réservées", self.dataPieceMecano);
                            pieceMecanoService.insertListePieceMecanoInHtml(core.qweb,self.dataPieceMecano);
                            self._render_is_click_button_Valid_all();
                        });
                    });
                }
                // console.log("Liste des pièces mécano", self.dataPieceMecano);
                
            });
        },
        _render_is_click_button_Valid_all : function (){
            const self = this;
            // this.$el.off('click', '.valid-all-button');
            if(pieceMecanoService.is_all_piece_checked(self.dataPieceMecano)) {
                console.log("Toute les pièces sont checkées");
              this.$el.find('.valid-all-button').prop('disabled', false);
            } else {
                console.log("Il reste des pièces à valider");
                this.$el.find('.valid-all-button').prop('disabled', true);
                
            }
        },
        _render_valid_all_button : function (){
            const self = this;
            this.$el.off('click', '.valid-all-button');
            this.$el.on('click', '.valid-all-button', function (e) {
                e.preventDefault();
                if (!pieceMecanoService.is_all_piece_denied(self.dataPieceMecano)) {
                    pieceMecanoService.validationCompleteStockPicking(self,self.dataPieceMecano, self.stock_piking_id,session, function (data) {
                        pieceMecanoService.showMessageSucces('message-valid-all-success');
                        self._show_listPieceMecano();
                    });    
                }else {
                    pieceMecanoService.annule_transfert(self, self.stock_piking_id, function (data) {
                        pieceMecanoService.showMessageSucces('message-valid-all-denied');
                        self._show_listPieceMecano();
                    });
                }                    
            });
        },
        _render_denied_button : function (){
            const self = this;
            this._render_click_button_check_piece(function (piece) {
                pieceMecanoService.deniedPieceMecanoStockMove(self, piece.stock_move_id[0], function (data) {
                    // console.log("Refus réussi", data);
                    // pieceMecanoService.showMessageSucces('message-denied-success');
                    // self._show_listPieceMecano();
                    self._show_listPieceMecano()
                });
            }, 'denied-button');
        },
        _render_valid_button : function (){
            const self = this;
            this._render_click_button_check_piece(function (piece) {
                console.log("Validation de la pièce mécano", piece);
                // pieceMecanoService.update_quantity_done_stock_move(self,piece, function (data) {
                // console.log("Mise à jour de la quantité effectuée", data);
                pieceMecanoService.validPieceMecanoStockMove(self, piece.stock_move_id[0], function (data) {
                    // console.log("Validation réussie", data);
                    // pieceMecanoService.showMessageSucces('message-valid-success');
                    // self._show_listPieceMecano();
                    self._show_listPieceMecano()
                });
                // });

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