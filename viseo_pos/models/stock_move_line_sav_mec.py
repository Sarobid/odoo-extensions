from odoo import models, fields, api
from datetime import datetime
class stock_move_line_sav_mec(models.Model):
    _name = "stock.move.line.sav.mec"
    _description = "Suivie de la validation des pieces atelier recu par le mecanicien"

    stock_move_line_id = fields.Many2one("stock.move.line", string="Ligne de mouvement de stock")
    state = fields.Selection([
        ('valid', 'Validé'),
        ('denied', 'Refusé')
    ], string="État", default='')
    date_done = fields.Datetime(string="Date de validation ou refus", default=datetime.now)

    def _get_value_selection_state(self):
        return dict(self._fields['state'].selection).get(self.state, 'Validation en attente')
    
    @api.model
    def validate_stock_move_line_mecano(self, stock_move_line_id):
        print("validate_stock_move_line_mecano", stock_move_line_id)
        stock_move_line = self.env['stock.move.line'].sudo().search(
            [("id","=",stock_move_line_id)]
        )

        print("stock_move_line", stock_move_line.id)
        if stock_move_line:
            print("stock_move_line found", stock_move_line)
            self.create({
                'stock_move_line_id': stock_move_line.id,
                'state': 'valid',
                'date_done': datetime.now()
            })
            stock_move_line.update_state_sav_mec('valid')
            return {"status": "200", "message": "Stock move line validated successfully."}
        else:
            return {"status": "404", "message": "Stock move line not found."}   

    @api.model
    def deny_stock_move_line_mecano(self, stock_move_line_id):
        stock_move_line = self.env['stock.move.line'].sudo().search(
            [("id","=",stock_move_line_id)]
        )
        if stock_move_line:
            self.create({
                'stock_move_line_id': stock_move_line.id,
                'state': 'denied',
                'date_done': datetime.now()
            })
            stock_move_line.update_state_sav_mec('denied')
            return {"status": "200", "message": "Stock move line denied successfully."}
        else:
            return {"status": "404", "message": "Stock move line not found."}