from odoo import models, fields, api

class hr_employee_service_product_list_rel(models.Model):
    _inherit = "hr_employee.service.product.list.rel"
    _description = "Relation entre le table employe et service_product_list"

