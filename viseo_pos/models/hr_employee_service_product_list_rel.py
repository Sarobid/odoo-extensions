from odoo import models, fields, api
from datetime import datetime

class hr_employee_service_product_list_rel(models.Model):
    _name = "hr_employee.service.product.list.rel"
    _description = "Relation entre le table employe et service_product_list"

    service_product_list_id = fields.Many2one("service.product.list",string="Srvice product list")
    hr_employee_id = fields.Many2one("hr.employee",string="Srvice product list")
    date_start_service = fields.Datetime(string="Date time start")
    date_end_service = fields.Datetime(string="Date time end")

    @api.model
    def commencer(self, service_id):
        print("commencer", service_id)
        if service_id:
            service_product_list = self._get_service_product_list_hr(service_id)
            print("Résultat de la recherche :", service_product_list)
            if service_product_list and not service_product_list.date_start_service:
                print("Date modifiée")
                service_product_list.write({
                    "date_start_service": datetime.now()
                })
                self._update_service_product_list_time(service_id)
        return {"status": "200"}

    def get_follow_state(self):
        status = "Non demarré"
        color = "#6c757d"
        if self.date_start_service:
            status = "Demarré"
            color = "#007bff"
            if self.date_end_service:
                status = "Terminé"
                color = "#28a745"
            followState =  self.env["follow.hr.emp.service.prod"].search([
                        ('hr_emp_service_prod_id', '=', self.ids),
                        ('date_end', '=', None),
                        ('date_start', '!=', None)
                    ], limit=1)
            if followState:
                status = followState.get_state_follow_name()
                color = followState.get_state_follow_color()
        return  {"status":status,"color":color}

    @api.model
    def _get_service_product_list_hr(self,service_id):
        return self.env['hr_employee.service.product.list.rel'].search([
            ('service_product_list_id', '=', service_id),
            ('hr_employee_id', '=', self.env.user.employee_id.id)
        ], limit=1)

    @api.model
    def _update_service_product_list_time(self,service_id):
        service_product = self.env['service.product.list'].search([
            ('id', '=', service_id),
        ], limit=1)
        service_product._update_time_done_date_start_end()

    @api.model
    def terminer(self, service_id):
        print("terminer", service_id)
        if service_id:
            service_product_list = service_product_list = self._get_service_product_list_hr(service_id)
            print("Résultat de la recherche :", service_product_list)
            if service_product_list and service_product_list.date_start_service and not service_product_list.date_end_service:
                print("Date modifiée")
                service_product_list.write({
                    "date_end_service": datetime.now()
                })
            self._update_service_product_list_time(service_id)
        return {"status": "200"}
    
    @api.model
    def _add_missing_id_column(self):
        self.env.cr.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'hr_employee_service_product_list_rel'
                    AND column_name = 'id'
                ) THEN
                    ALTER TABLE hr_employee_service_product_list_rel
                    ADD COLUMN id SERIAL PRIMARY KEY;
                END IF;
            END
            $$;
        """)

    @api.model
    def init(self):
        self._add_missing_id_column()


