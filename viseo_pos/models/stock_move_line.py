from odoo import models, api, fields
from datetime import datetime
class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    picking_product_line_sav_id = fields.One2many(
        'picking.product.line',
        inverse_name='picking_sav',
        string="Lignes de picking SAV",
    )
    def send_log_message_sav(self, textColor, rep_validation, stock_move_line_id):
        product = stock_move_line_id.product_id
        product_name = product.display_name or "Produit inconnu"
        product_code = product.default_code or ""
        qty = stock_move_line_id.qty_done or 0
        uom = stock_move_line_id.product_uom_id.name or ""

        message = f"""
            <ul style="padding-left: 16px;">
                <li>
                    à <strong style="color:{textColor};">{rep_validation}</strong> – l'article 
                    <strong>{product_name} ({product_code})</strong>, 
                    quantité : <strong>{qty} {uom}</strong>
                </li>
            </ul>
        """

        self.message_post(
            body=message,
            subject=f"[SAV Mécanicien] {rep_validation}"
        )



class stock_move_line(models.Model):
    _inherit = 'stock.move.line'

    state_sav_mec = fields.Selection(
        selection=[
            ('en_attente_validation', 'En attente'),
            ('valid', 'Validé'),
            ('denied', 'Refusé')
        ],
        string="État SAV Mécanicien",
        default='en_attente_validation',
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

    
    @api.model
    def create(self, vals):
        record = super(stock_move_line, self).create(vals)
        if record.is_sav_mec:
            self.send_message_sav_mec_piece_refresh()
        return record
    

    def write(self, vals):
        res = super(stock_move_line, self).write(vals)
        for record in self:
            if record.is_sav_mec:
                record.send_message_sav_mec_piece_refresh()
    
    def send_message_sav_mec_piece_refresh(self):
        print("stock_move_line send_message_sav_mec_piece_refresh")
        id = self.env.ref('viseo_pos.action_client_list_piece_mecano_id').id
        print("stock_move_line send_message_sav_mec_piece_refresh id", id)
        self.env['bus.bus'].sendone('sav_mec_piece_refresh', {
            'type': 'notification',
            'message': str(id),
        })
        
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
        self.picking_id.send_log_message_sav(
            textColor=self._get_color_state(state),
            rep_validation=dict(self._fields['state_sav_mec'].selection).get(state, 'Validation en attente'),
            stock_move_line_id=self
        )

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
