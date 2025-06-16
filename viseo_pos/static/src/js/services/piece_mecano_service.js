const pieceMecanoService = {
    getAllListePieceMecano: function (odooClient,traiteData) {
        return odooClient._rpc({
            model: 'v.pieces.atelier.done',
            method: 'search_read',
            args: [
                [['num_picking', '=', 1]],
                ['id','num_picking', 'name2', 'picking_sav', 'stock_move_id','product_id','product_uom_qty','product_uom_id','state_sav_mec','reserved_availability'],
            ],
        }).then(data => {
             console.log("Liste des pièces mécano", data);
            traiteData(pieceMecanoService.sortByDate(data));
        }).catch(error => {
            console.error("Erreur chargement", error);
        });
    },
    getPiecesSelected : function (dataPiece,id){
        return dataPiece.filter(piece => piece.id === id);
    },   
    get_piece_reserverd_availability_is_valid : function (data) {
        return data.filter(piece => piece.reserved_availability == piece.product_uom_qty);
    },
    update_quantity_done_stock_move : function (odooClient, piece,traiteData) {
        let quantity_done = piece.product_uom_qty;
        let stock_move_id = piece.stock_move_id[0];

        return odooClient._rpc({
            model: 'stock.move',
            method: 'write',
            args: [[stock_move_id], {
                quantity_done: quantity_done
            }],
        }).then(data => {
            traiteData(data);
        }).catch(error => {
            console.error("Erreur validation", error);
        });
    },
    validPieceMecanoStockMove: function (odooClient, stock_move_id,traiteData) {
        return odooClient._rpc({
            model: 'stock.move',
            method: 'validation_stock_move_mecano',
            args: [stock_move_id],
        }).then(data => {
            // console.log("Validation réussie", data);
            traiteData(data);
        }).catch(error => {
             console.error("Erreur validation", error);
        });
    },
    deniedPieceMecanoStockMove: function (odooClient, stock_move_id, traiteData) {
        return odooClient._rpc({
            model: 'stock.move',
            method: 'denied_stock_move_mecano',
            args: [stock_move_id],
        }).then(data => {
            // console.log("Refus réussi", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur refus", error);
        });
    },

    insertListePieceMecanoInHtml: function (qweb, data) {
        this.addTitlePiece(data)
        const html = qweb.render('PageListPieceMecano', { dataPieces: data });
        document.getElementById("piece-list-container").innerHTML = html;
    },
    addTitlePiece : function(data){
        let rmaname = "aucune pieces";
        let stockPickingName = "";
        if(data && data.length > 0){
            rmaname = data[0].name2;
            stockPickingName = data[0].picking_sav[1]
        }
        document.getElementById("rma-id-piece").textContent = rmaname;
        document.getElementById("stock-picking-id-piece").textContent = stockPickingName;

    },
    sortByDate: function (data) {
        return data.sort((a, b) => new Date(b.date_done) - new Date(a.date_done));
    },
    showMessageSucces: function (aletrClass) {
        console.log("Show message success", aletrClass);
        const messageElement = document.getElementById(aletrClass);
        if (messageElement) {
            messageElement.style.display = "block";
            setTimeout(() => {
                messageElement.style.display = "none";
            }, 3000);
        }
    },
    verificationDisponibilite: function (odooClient,stock_piking,company_id,traiteData) {
        console.log("Vérification disponibilité pour le stock picking", stock_piking);
        return odooClient._rpc({
            model: 'stock.picking',
            method: 'action_assign',
            args: [[stock_piking]],
            context: {
                'company_id': company_id,
            }
        }).then(data => {
            console.log("Vérification disponibilité réussie", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur vérification disponibilité", error);
        });
    },
    validationStockPicking: function (odooClient, stock_piking, traiteData) {
        return odooClient._rpc({
            model: 'stock.picking',
            method: 'button_validate',
            args: [[stock_piking]],
        }).then(data => {
            console.log("Validation stock picking réussie", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur validation stock picking", error);
        });
    },
    mettre_pas_relicas : function (odooClient,res_id,stock_piking, traiteData) {
        return odooClient._rpc({
            model: 'stock.backorder.confirmation',
            method: 'process_cancel_backorder',
            args: [[res_id]],
            context: {
                'active_id': stock_piking,
                'active_ids': [stock_piking],
                'active_model': 'stock.picking',
            }
        }).then(data => {
            console.log("Mise à jour des réplicas réussie", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur mise à jour des réplicas", error);
        });
    },
    transfertImmediate: function (odooClient,res_id, stock_piking, traiteData) {
        return odooClient._rpc({
            model: 'stock.immediate.transfer',
            method: 'process',
            args: [[res_id]],
            context: {
                'active_id': stock_piking,
                'active_ids': [stock_piking],
                'active_model': 'stock.picking',
            }
        }).then(data => {
            console.log("Transfert immédiat réussi", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur transfert immédiat", error);
        });
    },
    validationCompleteStockPicking: function (odooClient,dataMecano, stock_piking,session, traiteData) {
        console.log("session", session);
        pieceMecanoService.validationDesPiecesMecanoValid(odooClient,dataMecano,(rep)=>{
            pieceMecanoService.validationStockPicking(odooClient, stock_piking, function (data) {
                if (data && data['res_model'] && data['res_model'] === 'stock.immediate.transfer') {
                    pieceMecanoService.transfertImmediate(odooClient,data['res_id'], stock_piking, function (data) {
                        traiteData(data);
                    });
                }else {
                    if (data && data['res_model'] && data['res_model'] === 'stock.backorder.confirmation') {
                        pieceMecanoService.mettre_pas_relicas(odooClient,data['res_id'],stock_piking, function (data) {
                            traiteData(data);
                        });
                    }else {
                        traiteData(data);
                    }
                }
            });
        })
    },
    validationDesPiecesMecanoValid: function (odooClient,data,traiteData) {
        let dataTRaite =  data.filter(piece => piece.state_sav_mec === 'valid');
        return new Promise((resolve, reject) => {
            let promises = []
            for (let i = 0; i < dataTRaite.length; i++) {
                const piece = dataTRaite[i];
                promises.push(new Promise((resolve, reject) => {
                    this.update_quantity_done_stock_move(odooClient,piece,(data)=>{
                        console.log("update_quantity_done_stock_move")
                        resolve()
                    })
                }));
            }
            Promise.all(promises)
                .then(() => {
                    console.log("Toutes les pièces validées avec succès");
                    traiteData(dataTRaite);
                    resolve(dataTRaite);
                })
                .catch(error => {
                    console.error("Erreur lors de la validation des pièces", error);
                    reject(error);
                });
        })
    },
    is_all_piece_denied: function (data) {
        return data.every(piece => piece.state_sav_mec === 'denied');
    },
    is_all_piece_checked: function (data) {
        return data.every(piece => piece.state_sav_mec === 'valid' || piece.state_sav_mec === 'denied');
    },
    annule_transfert: function (odooClient, stock_piking, traiteData) {
        return odooClient._rpc({
            model: 'stock.picking',
            method: 'action_cancel',
            args: [[stock_piking]],
        }).then(data => {
            console.log("Annulation du transfert réussie", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur annulation du transfert", error);
        });
    }
}