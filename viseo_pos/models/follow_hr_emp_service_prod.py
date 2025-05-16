from odoo import models, fields, api
from datetime import datetime
class follow_hr_emp_service_prod(models.Model):
    _name = "follow.hr.emp.service.prod"
    _description = "Suivie blocage et pause du reparation des taches mecano"

    hr_emp_service_prod_id = fields.Many2one("hr_employee.service.product.list.rel",string="Service mecano")
    state_follow = fields.Selection([
        ('block', 'Bloquer'),
        ('break', 'Pause')
        ])
    date_start = fields.Datetime(string="Date debut")
    date_end = fields.Datetime(string="Date fin")

    @api.model
    def start_break(self,hr_emp_service_prod_id):
        return self.create_start_follow(hr_emp_service_prod_id,"break")

    @api.model
    def start_block(self,hr_emp_service_prod_id):
        return self.create_start_follow(hr_emp_service_prod_id,"block")

    @api.model
    def end_block(self,hr_emp_service_prod_id):
        return self.update_end_follow(hr_emp_service_prod_id,"block")

    @api.model
    def end_break(self,hr_emp_service_prod_id):
        return self.update_end_follow(hr_emp_service_prod_id,"break")

    def _get_follow_hr(self,hr_emp_service_prod_id,state_follow):
        return self.env['follow.hr.emp.service.prod'].search([
            ('hr_emp_service_prod_id', '=', hr_emp_service_prod_id),
            ('date_end', '=', None),
            ('date_start', '!=', None),
            ('state_follow', '=', state_follow)
        ], limit=1)

    @api.model
    def create_start_follow(self,hr_emp_service_prod_id,state_follow):
        follow_hr = self._get_follow_hr(hr_emp_service_prod_id,state_follow)
        if follow_hr :
            message = f"""{state_follow} already started with {follow_hr.date_start}"""
            print(message)
            return {"status":"406","message":message}
        else:
            follow_hr = self.create({
                "hr_emp_service_prod_id":hr_emp_service_prod_id,
                "state_follow":state_follow,
                "date_start": datetime.now()
            })
            follow_hr = self._get_follow_hr(hr_emp_service_prod_id, state_follow)
            fleet = follow_hr._get_fleet_vehicle_log_services()
            fleet.update_more_nbr_service_product(state_follow)
            fleet.send_log_message_follow_hr(state_follow=state_follow,operation_name=follow_hr.hr_emp_service_prod_id.service_product_list_id.operation_done)
            return {"status":"201","message":"Created"}

    @api.model
    def update_end_follow(self,hr_emp_service_prod_id,state_follow):
        follow_hr = self._get_follow_hr(hr_emp_service_prod_id,state_follow)
        if follow_hr :
            follow_hr.write({
                "date_end":datetime.now()
            })
            fleet = follow_hr._get_fleet_vehicle_log_services()
            fleet.update_less_nbr_service_product(state_follow)
            fleet.send_log_message_unfollow_hr(state_follow=state_follow,operation_name=follow_hr.hr_emp_service_prod_id.service_product_list_id.operation_done)
            return {"status":"200","message":""}
        else:
            message = f"""un{state_follow} not acceptable"""
            print(message)
            return {"status":"406","message":message}

    @api.model
    def _get_fleet_vehicle_log_services(self):
        # product_list_id
        print("_get_fleet_vehicle_log_services")
        print(self.hr_emp_service_prod_id.service_product_list_id)
        fleet_vehicle_log_services = self.env['fleet.vehicle.log.services'].search([
            ('product_list_id', '=', self.hr_emp_service_prod_id.service_product_list_id.id)]
            ,limit=1)
        print(fleet_vehicle_log_services)
        return fleet_vehicle_log_services