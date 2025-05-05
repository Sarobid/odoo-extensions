from odoo import models, fields, api

class vehicle_employee(models.Model):
    _name = "v.smart.vehicle.employee"
    _description = "RMA view of employee vehicles"
    _auto = False

    id = fields.Integer(string="ID", readonly=True) #rma id
    name2 = fields.Char(String="Réference de réparation") #reference de reparation
    vehicle_id = fields.Many2one("fleet.vehicle",string="Véhicule")
    hr_employee_id = fields.Many2one("hr.employee",string="Employée")

    @api.model
    def _query(self):
        return """
        select 
            distinct
            a.id + d.hr_employee_id as id, 
            a.name2,
            f.vehicle_id,
            d.hr_employee_id 
        from fleet_vehicle_log_services a
		join fleet_vehicle_cost f on f.id=a.cost_id
		join fleet_vehicle b on f.vehicle_id=b.id
        join service_product_list c on c.repair_id=a.id
        join hr_employee_service_product_list_rel d on d.service_product_list_id=c.id
        JOIN hr_employee g on g.id= d.hr_employee_id
        where g.active is true
            """

    def init(self):
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")