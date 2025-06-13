const pieceMecanoService = {
    getAllListePieceMecano: function (odooClient,traiteData) {
        return odooClient._rpc({
            model: 'v.pieces.atelier.done',
            method: 'search_read',
            args: [
                [['num_picking', '=', 1]],
                ['id','num_picking', 'name2', 'picking_sav', 'stock_move_id','product_id','product_uom_qty','product_uom_id'],
            ],
        }).then(data => {
            traiteData(pieceMecanoService.sortByDate(data));
        }).catch(error => {
            console.error("Erreur chargement", error);
        });
    },
    getPiecesSelected : function (dataPiece,id){
        return dataPiece.filter(piece => piece.id === id);
    },
    validPieceMecano: function (odooClient, stock_move_line_id,traiteData) {
        return odooClient._rpc({
            model: 'stock.move.line.sav.mec',
            method: 'validate_stock_move_line_mecano',
            args: [stock_move_line_id],
        }).then(data => {
            // console.log("Validation réussie", data);
            traiteData(data);
        }).catch(error => {
            // console.error("Erreur validation", error);
        });
    },
    deniedPieceMecano: function (odooClient, stock_move_line_id, traiteData) {
        return odooClient._rpc({
            model: 'stock.move.line.sav.mec',
            method: 'deny_stock_move_line_mecano',
            args: [stock_move_line_id],
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
    validationCompleteStockPicking: function (odooClient, stock_piking,session, traiteData) {
        console.log("session", session);
        this.verificationDisponibilite(odooClient, stock_piking,session.company_id, function (data) {
            pieceMecanoService.validationStockPicking(odooClient, stock_piking, function (data) {
                if (data && data['res_model'] && data['res_model'] === 'stock.immediate.transfer') {
                    pieceMecanoService.transfertImmediate(odooClient,data['res_id'], stock_piking, function (data) {
                        traiteData(data);
                    });
                }else {
                    traiteData(data);
                }
            });
        })
    }
}