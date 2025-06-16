from odoo import models, api, fields
from datetime import datetime
class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    picking_product_line_sav_id = fields.One2many(
        'picking.product.line',
        inverse_name='picking_sav',
        string="Lignes de picking SAV",
    )



class stock_move(models.Model):
    _inherit = 'stock.move'

    state_sav_mec = fields.Selection(
        selection=[
            ('en_attente_validation', 'En attente'),
            ('valid', 'Validé'),
            ('denied', 'Refusé')
        ],
        string="État SAV Mécanicien"
    )
    date_sav_mec = fields.Datetime(
        string="Date SAV Mécanicien",
    )
    state_sav_mec_display = fields.Char(
        string="État SAV Mécanicien Affichage",
        default = lambda self: self._create_state_sav_mec_display(self.state_sav_mec),
    )
    is_sav_mec = fields.Boolean(
        string="Est un SAV Mécanicien",
        default=False,
        help="Indique si cette ligne de mouvement de stock est liée à un SAV Mécanicien.",
        compute="_compute_is_sav_mec",
        store=False
    )
   
    @api.depends("picking_id")
    def _compute_is_sav_mec(self):
        for record in self:
            record.is_sav_mec = False
            if record.picking_id:
                if record.picking_id.picking_product_line_sav_id:
                    record.is_sav_mec = True
            print("stock_move_line _compute_is_sav_mec", record)

    @api.model
    def update_state_sav_mec(self, state):
        html = self._create_state_sav_mec_display(state)
        self.write({
            'state_sav_mec': state,
            'date_sav_mec': datetime.now()
            ,'state_sav_mec_display': html
        })
    
    @api.model
    def validation_stock_move_mecano(self, stock_move_id):
        print("validation_stock_move_mecano", stock_move_id)
        stock_move = self.sudo().search(
            [("id", "=", stock_move_id)]
        )
        print("stock_move", stock_move.id)
        if stock_move:
            print("stock_move found", stock_move)
            stock_move.update_state_sav_mec('valid')
            return {"status": "200", "message": "Stock move validated successfully."}
        else:
            return {"status": "404", "message": "Stock move not found."}
        
    @api.model
    def denied_stock_move_mecano(self, stock_move_id):
        print("denied_stock_move_mecano", stock_move_id)
        stock_move = self.sudo().search(
            [("id", "=", stock_move_id)]
        )
        print("stock_move", stock_move.id)
        if stock_move:
            print("stock_move found", stock_move)
            stock_move.update_state_sav_mec('denied')
            return {"status": "200", "message": "Stock move validated successfully."}
        else:
            return {"status": "404", "message": "Stock move not found."}

    

    def _get_value_selection_state_sav_mec(self):
        return dict(self._fields['state_sav_mec'].selection).get(self.state_sav_mec, 'Validation en attente')
    

    def _get_color_state(self,state_sav_mec):
        color = "#6c757d"
        if state_sav_mec == 'valid':
            color = "#28a745"
        elif state_sav_mec == 'denied':
            color = "#dc3545"
        return color
    
    def _create_state_sav_mec_display(self, state):
        state_label = dict(self._fields['state_sav_mec'].selection).get(state, 'Validation en attente')
        color = self._get_color_state(state)
        html = (
            f"<div style='line-height: 1.6;'>"
            f"  <div style='margin-bottom: 4px;'>"
            f"    <span style='"
            f"        background-color: {color};"
            f"        color: white;"
            f"        padding: 2px 6px;"
            f"        border-radius: 6px;"
            f"        font-size: 12px;"
            f"        margin-right: 6px;'>"
            f"      {state_label}</span>"
            f"  </div>"
            f"</div>"
        )
        return html
