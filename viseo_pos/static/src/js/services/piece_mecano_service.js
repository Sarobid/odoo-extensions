const pieceMecanoService = {
    getAllListePieceMecano: function (odooClient,traiteData) {
        return odooClient._rpc({
            model: 'v.pieces.atelier.done',
            method: 'search_read',
            args: [
                [],
                ['id', 'name2', 'picking_sav', 'stock_move_line_id','product_id','qty_done','product_uom_id','date_done','date_done'],
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
        const html = qweb.render('PageListPieceMecano', { dataPieces: data });
        document.getElementById("piece-list-container").innerHTML = html;
    },
    sortByDate: function (data) {
        return data.sort((a, b) => new Date(b.date_done) - new Date(a.date_done));
    },
    showMessageSucces: function (aletrClass) {
        const messageElement = document.getElementById(aletrClass);
        if (messageElement) {
            messageElement.style.display = "block";
            setTimeout(() => {
                messageElement.style.display = "none";
            }, 3000);
        }
    },
}