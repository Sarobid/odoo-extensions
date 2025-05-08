from odoo import models, fields, api

class v_service_product_list(models.Model):
    _name = "v.service.product.list"
    _description = "RMA view of employee vehicles"
    _auto = False

    id = fields.Integer(string="ID", readonly=True) #rma id
    namelibre = fields.Char(string="namelibre")
    operation_done = fields.Char(string="operation à effectuee")
    product_id = fields.Many2one("product.product",string="Article")
    product_qty = fields.Float(string=" Quantite article")
    repair_id = fields.Many2one("fleet.vehicle.log.services",string="RMA vehicle")
    service_work_id = fields.Many2one("fleet.service.work",string="Type de travaux")

    @api.model
    def _query(self):
        return """
        select 
            a.id,
            a.name as namelibre,
            a.operation_done, --operation à effectuee
            a.product_id, --piece
            a.product_qty, --quantité piece
            a.repair_id, --rma id
            b.service_work_id -- type de travaux
            from service_product_list a 
            join fleet_vehicle_log_services b on b.id=a.repair_id
            """

    def init(self):
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")