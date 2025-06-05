from odoo import models, fields

class v_pieces_atelier_done(models.Model):
    _name = "v.pieces.atelier.done"
    _description = "List of vehicle parts received by the after-sales service workshop to be validated by the mechanic"
    _auto = False
    _order = "date_done desc"

    id = fields.Integer(string="ID", readonly=True) #rma id
    name2 = fields.Char(String="Réference de réparation") #reference de reparation
    picking_sav = fields.Many2one("stock.picking", string="Picking SAV")
    stock_move_line_id = fields.Many2one("stock.move.line", string="Ligne de mouvement de stock")
    product_id = fields.Many2one("product.product", string="Produit")
    qty_done = fields.Integer(string="Quantité")
    product_uom_id = fields.Many2one("uom.uom", string="Unité de mesure")
    date_done = fields.Datetime(string="Date effective")

    def _query(self):
        return """
        select
            row_number() over () as id, 
            b.id as rma_id,
            b.name2,
            a.picking_sav,
            c.name as stock_picking_name,
            c.state,
            e.id as stock_move_line_id,
            e.product_id,
            e.qty_done,
            e.product_uom_id,
            c.date_done
        from picking_product_line a
            join fleet_vehicle_log_services b on b.id=a.repair_id and b.state_ro='diag' and b.is_transfert_done is false
            join stock_picking c on c.id=a.picking_sav 
                and (c.state='done')
            join stock_move_line e on (e.picking_id = c.id and e.state_sav_mec !='valid' and e.state_sav_mec != 'denied')
        where 
			a.picking_return_mg is null 
			and a.picking_return_sav is null 
            """
    
    def init(self):
        self.env.cr.execute(f"""DROP VIEW IF EXISTS {self._table} """)
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")