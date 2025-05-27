from odoo import models, fields, api
from datetime import datetime

from viseo_13.viseo_custom_dashboard.models.model_methods import print_all


class hr_employee_service_product_list_rel(models.Model):
    _name = "hr_employee.service.product.list.rel"
    _description = "Relation entre le table employe et service_product_list"

    service_product_list_id = fields.Many2one("service.product.list",string="Srvice product list")
    hr_employee_id = fields.Many2one("hr.employee",string="Srvice product list")
    date_start_service = fields.Datetime(string="Date time start")
    date_end_service = fields.Datetime(string="Date time end")

    def _get_heure_travail(self):
        self.env.cr.execute("""select date_start,date_end from follow_hr_emp_service_prod a where a.hr_emp_service_prod_id=%s order by date_start asc""",(self.id,))
        result = self.env.cr.fetchall()
        array_htravail = []
        if self.date_start_service:
            dstart = self.date_start_service
            dend = datetime.now()
            for tmp_stop in result:
                dend = tmp_stop[0]
                array_htravail.append(self.calcul_heure_travail(dstart,dend))
                if tmp_stop[1] is not None:
                    dstart = tmp_stop[1]
                else:
                    dstart = datetime.now()
            if self.date_end_service:
                dend = self.date_end_service
            else:
                dend = datetime.now()
            array_htravail.append(self.calcul_heure_travail(dstart,dend))
        return array_htravail

    def calcul_heure_travail(self,dstart,dend):
        return {"start":dstart,"end":dend,"diff":(dend - dstart).total_seconds()}

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


