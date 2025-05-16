from odoo import models, fields, api

class fleet_vehicle_log_services(models.Model):
    _inherit = "fleet.vehicle.log.services"

    nbr_service_product_block = fields.Integer(string="nombre d'employe bloquer")
    nbr_service_product_break = fields.Integer(string="nombre d'employe en  pause")

    @api.model
    def update_more_nbr_service_product(self,follow_hr):
        if follow_hr == "block":
            self.update_more_nbr_service_product_block()
        else:
            self.update_more_nbr_service_product_break()

    @api.model
    def update_less_nbr_service_product(self,follow_hr):
        if follow_hr == "block":
            self.update_less_nbr_service_product_block()
        else:
            self.update_less_nbr_service_product_break()

    @api.model
    def update_more_nbr_service_product_block(self):
        self.write({
            "nbr_service_product_block":self.nbr_service_product_block + 1
        })

    @api.model
    def update_less_nbr_service_product_block(self):
        self.write({
            "nbr_service_product_block": self.nbr_service_product_block - 1
        })

    @api.model
    def update_more_nbr_service_product_break(self):
        self.write({
            "nbr_service_product_break": self.nbr_service_product_break + 1
        })

    @api.model
    def update_less_nbr_service_product_break(self):
        self.write({
            "nbr_service_product_break": self.nbr_service_product_break - 1
        })

    def send_log_message_follow_hr(self, state_follow, operation_name):
        if state_follow == "block":
            if operation_name is None or operation_name == False:
                operation_name = ""
            self.send_log_message_follow(textcolor="red",message=f"{operation_name} bloqué", operation_name=operation_name)

    def send_log_message_unfollow_hr(self, state_follow, operation_name):
        if state_follow == "block":
            if operation_name is None or operation_name == False:
                operation_name = ""
            self.send_log_message_follow(textcolor="green",message=f"{operation_name} débloqué", operation_name=operation_name)

    def send_log_message_follow(self, textcolor, message, operation_name):
        body_message = ("""
            <div class='col-xs-6'>
                <ul>
                    <li style='color:%s'><i>%s</i></li>
                </ul>
            </div>
        """ % (textcolor, message))
        self.message_post(body=body_message, subject=operation_name)

    

