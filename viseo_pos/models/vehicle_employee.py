from odoo import models, fields

class vehicle_employee(models.Model):
    _name = "v.smart.vehicle.employee"
    _description = "RMA view of employee vehicles"
    _auto = False

    id = fields.Integer(string="ID", readonly=True) #rma id
    name2 = fields.Char(String="Réference de réparation") #reference de reparation
    vehicle_id = fields.Many2one("fleet.vehicle",string="Véhicule")
    hr_employee_id = fields.Many2one("hr.employee",string="Employée")
    license_plate = fields.Char(String="Immatriculation")
    vin_sn = fields.Char(String="Numéro VIN")
    brand_id = fields.Many2one("fleet.vehicle.model.brand",string="Marque")
    model_id = fields.Many2one("fleet.vehicle.model",string="Modeles")
    user_id = fields.Many2one("res.users",string="Utilisateurs")
    rma_id = fields.Integer(String="ID RMA")
    vehicle_type = fields.Many2one("fleet.vehicle.model",string="Type")
    number_task = fields.Integer(string="nombre tache assignee")
    task_end = fields.Integer(string="nombre tache treminee")
    is_task_no_end = fields.Boolean(string="Exist-il de tache ?")
    state_ro = fields.Char(String="STATUS")
    customer_id = fields.Many2one("res.partner",string="Client")
    
    def _query(self):
        return """
        select     
            row_number() over () as id, 
            a.name2,
            a.id as rma_id,
            f.vehicle_id,
            d.hr_employee_id ,
			b.license_plate,
			b.vin_sn,
			b.brand_id,
			h.name as name_marque,
			b.model_id,
			i.name as name_model_type,
            g.user_id,
			i.vehicle_type,
			COUNT(*) AS number_task,
			SUM(CASE WHEN d.date_start_service is not null and d.date_end_service is not null then 1
			else 0 end) as task_end,
            (COUNT(*) != SUM(CASE WHEN d.date_start_service is not null and d.date_end_service is not null then 1 else 0 end)) as is_task_no_end,
            a.state_ro,
            a.customer_id
        from fleet_vehicle_log_services a
		join fleet_vehicle_cost f on f.id=a.cost_id
		join fleet_vehicle b on f.vehicle_id=b.id
        join service_product_list c on c.repair_id=a.id
        join hr_employee_service_product_list_rel d on d.service_product_list_id=c.id
        JOIN hr_employee g on g.id= d.hr_employee_id
		left join fleet_vehicle_model_brand h on h.id=b.brand_id
		left join fleet_vehicle_model i on i.id = b.model_id
		left join fleet_type_vehicle j on j.id=i.vehicle_type 
        where g.active is true
		GROUP BY 
			(
            a.name2,
            a.id ,
            f.vehicle_id,
            d.hr_employee_id ,
			b.license_plate,
			b.vin_sn,
			b.brand_id,
			h.name,
			b.model_id,
			i.name,
            g.user_id,
			i.vehicle_type,
            a.state_ro,
            a.customer_id)
            """
    
    def init(self):
        self.env.cr.execute(f"""DROP VIEW IF EXISTS {self._table} """)
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")