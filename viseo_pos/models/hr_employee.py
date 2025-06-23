from odoo import models, fields
import random

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    code_pin = fields.Char(
        string="Code PIN",
        help="Code PIN pour l'accès mobile de l'employé.",
        default="",
    )

    def generate_code_pin(self):
        for rec in self:
            code = rec._algo_generate_code_pin()
            rec.write({'code_pin': code})

    def _algo_generate_code_pin(self):
        while True:
            code_pin = ''.join(str(random.randint(0, 9)) for _ in range(4))
            if not self._code_pin_exists(code_pin):
                return code_pin

    def _code_pin_exists(self, code_pin):
        return self.env['hr.employee'].search_count([('code_pin', '=', code_pin)]) > 0
