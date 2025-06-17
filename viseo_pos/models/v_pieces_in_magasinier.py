from odoo import models, fields,api

class v_pieces_in_magasinier(models.Model):
    _name = "v.pieces.in.magasinier"
    _description = "Liste des pièces reçues par le magasinier pour l'atelier SAV"
    _auto = False

    id = fields.Integer(string="ID", readonly=True)
    name2 = fields.Char(String="Réference de réparation") 
    picking_sav = fields.Many2one("stock.picking", string="Picking SAV")
    stock_move_id = fields.Many2one("stock.move", string="Mouvement de stock")
    product_id = fields.Many2one("product.product", string="Produit")
    product_uom_qty = fields.Integer(string="Quantité")
    product_uom_id = fields.Many2one("uom.uom", string="Unité de mesure")
    state_sav_mec = fields.Char(string="État SAV Mécanicien")
    location_id = fields.Many2one("stock.location", string="Emplacement d'origine")
    location_dest_id = fields.Many2one("stock.location", string="Emplacement de destination")
    picking_magasinier = fields.Many2one("stock.picking", string="Picking Magasinier")
    quantity_done = fields.Integer(string="Quantité Fait", compute="_compute_quantity_done", store=False)
    
    @api.depends('stock_move_id')
    def _compute_quantity_done(self):
        for record in self:
            if record.stock_move_id :
                record.quantity_done = record.stock_move_id.quantity_done if record.stock_move_id.quantity_done else 0.0
            else:
                record.quantity_done = 0.0

    def _query(self):
        return """
            SELECT
                row_number() OVER (ORDER BY a.id, b.id, c.id, e.id) AS id, 
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
                c.location_id as location_id,
                c.location_dest_id as location_dest_id,
                a.picking_magasinier AS picking_magasinier             
            FROM picking_product_line a
            JOIN fleet_vehicle_log_services b 
                ON b.id = a.repair_id 
            JOIN stock_picking c 
                ON c.id = a.picking_magasinier 
                AND c.state = 'done'
            JOIN stock_move e 
                ON e.picking_id = c.id
            """
    
    def init(self):
        self.env.cr.execute(f"""DROP VIEW IF EXISTS {self._table} """)
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")