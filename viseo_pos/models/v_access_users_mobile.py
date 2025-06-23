from odoo import models, fields,api

class v_access_users_mobile(models.Model):
    _name = "v.access.users.mobile"
    _description = "Liste des utilisateurs lie aux employes pour l'acces mobile"
    _auto = False

    id = fields.Integer(string="ID", readonly=True)
    user_id = fields.Many2one("res.users", string="Utilisateur", readonly=True)
    code_pin = fields.Char(string="code_pin", readonly=True)
    login = fields.Char(string="Login", readonly=True)
    
    @api.model
    def connect_to_mobile(self, code_pin):
        print(f"Connecting to mobile with code_pin: {code_pin}")
        access_users_mobile = self.env['v.access.users.mobile'].search([('code_pin', '=', code_pin)], limit=1)
        if not access_users_mobile:
            return {'status': 404, 'error': 'User not found'}
        else:
            user = access_users_mobile.user_id
            return user.generate_token_mobile()

    def _query(self):
        return """
            select 
                row_number() OVER (ORDER BY a.id, b.id) AS id,
                a.code_pin,
                a.user_id,
                b.login
            from hr_employee a
            join res_users b on b.id=a.user_id
        """
    
    def init(self):
        self.env.cr.execute(f"""DROP VIEW IF EXISTS {self._table} """)
        self.env.cr.execute(f"""CREATE OR REPLACE VIEW {self._table} AS ({self._query()})""")