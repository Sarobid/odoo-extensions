from odoo import models, fields,api

class v_pieces_atelier_done(models.Model):
    _name = "v.pieces.atelier.done"
    _description = "List of vehicle parts received by the after-sales service workshop to be validated by the mechanic"
    _auto = False

    id = fields.Integer(string="ID", readonly=True)
    num_picking = fields.Integer(string="Numéro de picking dans cette view", readonly=True)
    name2 = fields.Char(String="Réference de réparation") 
    picking_sav = fields.Many2one("stock.picking", string="Picking SAV")
    stock_move_id = fields.Many2one("stock.move", string="Mouvement de stock")
    product_id = fields.Many2one("product.product", string="Produit")
    product_uom_qty = fields.Integer(string="Quantité")
    product_uom_id = fields.Many2one("uom.uom", string="Unité de mesure")
    state_sav_mec = fields.Char(string="État SAV Mécanicien")
    reserved_availability = fields.Integer(string="Quantité disponible réservée", compute="_compute_reserved_availability", store=False)
    
    @api.depends('stock_move_id')
    def _compute_reserved_availability(self):
        for record in self:
            if record.stock_move_id :
                record.reserved_availability = record.stock_move_id.reserved_availability if record.stock_move_id.reserved_availability else 0.0
            else:
                record.reserved_availability = 0.0

    def _query(self):
        return """
            SELECT
                row_number() OVER (ORDER BY a.id, b.id, c.id, e.id) AS id, 
                DENSE_RANK() OVER (ORDER BY c.id DESC) AS num_picking,
                b.id AS rma_id,
                b.name2,
                a.picking_sav,
                c.name AS stock_picking_name,
                c.state,
                e.id AS stock_move_id,
                e.product_id,
                e.product_uom_qty,
                e.product_uom as product_uom_id,
                e.state_sav_mec,
                0 AS reserved_availability                
            FROM picking_product_line a
            JOIN fleet_vehicle_log_services b 
                ON b.id = a.repair_id 
                AND b.state_ro = 'diag' 
                AND b.is_transfert_done IS FALSE
            JOIN stock_picking c 
                ON c.id = a.picking_sav 
                AND c.state = 'assigned'
            JOIN stock_move e 
                ON e.picking_id = c.id
            """
    
    def init(self):
        self.env.cr.execute(f"""DROP VIEW IF EXISTS {self._table} """)
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")