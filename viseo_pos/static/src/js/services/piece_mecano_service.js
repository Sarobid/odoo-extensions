const pieceMecanoService = {
    getAllListePieceMecano: function (odooClient,traiteData) {
        return odooClient._rpc({
            model: 'v.pieces.atelier.done',
            method: 'search_read',
            args: [
                [['num_picking', '=', 1]],
                ['id','num_picking', 'name2', 'picking_sav', 'stock_move_id','product_id','product_uom_qty','product_uom_id','state_sav_mec','location_id','location_dest_id','picking_magasinier','picking_product_line_id','reserved_availability'],
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
        console.log("get_piece_reserverd_availability_is_valid", data);
        return data.filter(piece => piece.reserved_availability == piece.product_uom_qty && piece.product_uom_qty > 0);
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
    },cancelPieceMecanoStockMove: function (odooClient, stock_move_id,traiteData) {
        return odooClient._rpc({
            model: 'stock.move',
            method: 'cancel_stock_move_mecano',
            args: [stock_move_id],
        }).then(data => {
            // console.log("Validation réussie", data);
            traiteData(data);
        }).catch(error => {
             console.error("Erreur annulation", error);
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
    },
    retourner_all_pieces_magasinier : function (odooClient,picking_magasinier,dataMecano,traiteData){
        let array_piece_refuser = dataMecano.filter(piece => piece.state_sav_mec === 'denied');
        this.getAllPieceInMagasin(odooClient,picking_magasinier, (data) => {
            let dataResult = []
            const picking_product_line_id = dataMecano[0].picking_product_line_id[0];
            for (let i = 0; i < data.length; i++) {
                const piece = data[i];
                for (let j = 0; j < array_piece_refuser.length; j++) {
                    const piece_refuser = array_piece_refuser[j];
                    if (piece.product_id[0] === piece_refuser.product_id[0]) {
                        console.log("Retourner pièce magasinier", piece, piece_refuser);
                        dataResult.push(piece)
                        break;
                    }
                }
            }
            if (dataResult.length > 0) {
                this.create_return_piece_magasinier(odooClient,picking_product_line_id, dataResult[0], dataResult, (data) => {
                    traiteData(data);
                });   
            }else {
                console.log("Aucune pièce à retourner au magasinier");
                traiteData({ message: "Aucune pièce à retourner au magasinier" });
            }
        })
    },
    create_return_piece_magasinier: function (odooClient, picking_product_line_id,picking_magasinier,array_produit_a_retourne, traiteData) {
        const product_return_moves = array_produit_a_retourne.map(prod => {
            return [0, 0, {
                product_id: prod.product_id[0],
                quantity: prod.quantity_done,
                move_id: prod.stock_move_id[0],
                to_refund: true
            }];
        });
        const picking_id = picking_magasinier.picking_magasinier[0];
        console.log("Création de retour de pièce magasinier", picking_id, product_return_moves);
        return odooClient._rpc({
            model: "stock.return.picking",
            method: "create",
            args: [{
                picking_id: picking_id,
                product_return_moves: product_return_moves,
                parent_location_id: picking_magasinier.location_dest_id[0],
                original_location_id: picking_magasinier.location_id[0],
                location_id: picking_magasinier.location_id[0],
            }],
            context: {
                active_model: "stock.picking",
                active_id: picking_id,
                active_ids: [picking_id]
            }
        }).then(data => {
            console.log("Mise à jour des pièces en magasinier réussie", data);
                pieceMecanoService.validation_create_return_piece_magasinier(odooClient, data, picking_magasinier, (data) => {
                    console.log("picking_product_line_id", picking_product_line_id);
                    pieceMecanoService.update_picking_return_mg_to_product_return(odooClient,picking_product_line_id,data['res_id'], (data) => {
                         traiteData(data);
                    });
                });
        }).catch(error => {
            console.error("Erreur mise à jour des pièces en magasinier", error);
        });
    },
    validation_create_return_piece_magasinier: function (odooClient, result_id,picking_magasinier, traiteData) {
        return odooClient._rpc({
            model: "stock.return.picking",
            method: "create_returns",
            args: [result_id],
            context: {
                active_model: "stock.picking",
                active_id: picking_magasinier.picking_magasinier[0],
                active_ids: [picking_magasinier.picking_magasinier[0]]
            }
        }).then(data => {
            console.log("Validation de la création de retour de pièce magasinier réussie", data);
            traiteData(data);
        }).catch(error => {
            console.error("Erreur validation création retour pièce magasinier", error);
        });
    },
    update_picking_return_mg_to_product_return: function (odooClient, picking_product_line_id, picking_return_id, traiteData) {
        console.log("Mise à jour de picking_product_line_id", picking_product_line_id, "avec picking_return_id", picking_return_id);
        return odooClient._rpc({
            model: 'picking.product.line',
            method: 'update_picking_return_mg_to_product_return',
            args: [picking_product_line_id, picking_return_id], // passer les arguments ici
        }).then(data => {
            console.log("Mise à jour de picking_product_line_id réussie", data);
            traiteData(data);
        }).catch(error => {

            console.error("Erreur Mise à jour de picking_product_line_id:", error);
        });
    },
    getAllPieceInMagasin: function (odooClient,picking_magasinier, traiteData) {
        return odooClient._rpc({
            model: 'v.pieces.in.magasinier',
            method: 'search_read',
            args: [
                [['picking_magasinier', '=', picking_magasinier]],
                ['id', 'name2', 'picking_sav', 'stock_move_id','product_id','product_uom_qty','product_uom_id','state_sav_mec','location_id','location_dest_id','picking_magasinier','quantity_done'],
            ],
        }).then(data => {
            console.log("Liste des pièces en magasin", data);
            traiteData(pieceMecanoService.sortByDate(data));
        }).catch(error => {
            console.error("Erreur chargement des pièces en magasin", error);
        });
    }

}