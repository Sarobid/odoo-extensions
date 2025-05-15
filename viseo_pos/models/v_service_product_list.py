from odoo import models, fields, api

class v_service_product_list(models.Model):
    _name = "v.service.product.list"
    _description = "RMA view of employee vehicles"
    _auto = False

    id = fields.Integer(string="ID")
    service_product_list_id = fields.Integer(string="service_product_list_id")
    namelibre = fields.Char(string="namelibre")
    operation_done = fields.Char(string="operation à effectuee")
    product_id = fields.Many2one("product.product",string="Article")
    product_qty = fields.Float(string=" Quantite article")
    # repair_id = fields.Many2one("fleet.vehicle.log.services",string="RMA vehicle")
    repair_id = fields.Integer(string="RMAID")
    service_work_id = fields.Many2one("fleet.service.work",string="Type de travaux")
    hr_employee_id = fields.Many2one("hr.employee",string="Employe")
    user_id = fields.Many2one("res.users",string="Utilisateur")
    date_start_service = fields.Datetime(string="Date time start")
    date_end_service = fields.Datetime(string="Date time end")
    state_follow = fields.Char(string="status de suivie (pause ou bloquer)")
    hr_employee_service_prod_list_id = fields.Integer(string="hr_employee_service_prod_list_id")

    @api.model
    def _query(self):
        return """
        select 
            row_number() over () as id,
			a.id as service_product_list_id,
            a.name as namelibre,
            a.operation_done, --operation à effectuee
            a.product_id, --piece
            a.product_qty, --quantité piece
            a.repair_id, --rma id
            b.service_work_id, -- type de travaux
        	c.hr_employee_id,
			d.user_id,
			c.date_start_service,
			c.date_end_service,
            e.state_follow,
            c.id as hr_employee_service_prod_list_id
		from service_product_list a 
            join fleet_vehicle_log_services b on b.id=a.repair_id
			left join hr_employee_service_product_list_rel c on c.service_product_list_id=a.id
			left join hr_employee d on d.id=c.hr_employee_id 
            left join follow_hr_emp_service_prod e on e.hr_emp_service_prod_id=c.id and e.date_end is null and e.date_start is not null
            """

    def init(self):
        self.env.cr.execute(f"""DROP VIEW IF EXISTS {self._table} """)
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")