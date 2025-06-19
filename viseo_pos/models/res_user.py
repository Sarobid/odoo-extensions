from odoo import models, api,fields
import secrets

class res_users(models.Model):
    _inherit = 'res.users'

    token_mobile = fields.Char(string="Token Mobile", readonly=True)

    @api.model
    def generate_token_mobile(self):
        self.token_mobile = secrets.token_hex(16)
        self.write({'token_mobile': self.token_mobile,'password': self.token_mobile})
        return {'status': 200, 'message': 'Token generated successfully', 'token_mobile': self.token_mobile}

    @api.model
    def create(self, vals):
        user = super(res_users, self).create(vals)
        user._restrict_menus_if_in_group(vals)
        return user

    def write(self, vals):
        res = super(res_users, self).write(vals)
        self._restrict_menus_if_in_group(vals)
        return res

    def _restrict_menus_if_in_group(self, vals):
        group_my_vehicles = self.env.ref('viseo_pos.group_rma_vehicle_mecano', raise_if_not_found=False)
        menu_my_vehicles = self.env.ref('viseo_pos.menu_my_vehicles_root', raise_if_not_found=False)
        menu_my_pieces = self.env.ref('viseo_pos.menu_list_piece_mecano_root', raise_if_not_found=False)

        if not group_my_vehicles or not menu_my_vehicles or not menu_my_pieces:
            return

        group_flag = f'in_group_{group_my_vehicles.id}'

        if group_flag in vals:
            for user in self:
                if vals[group_flag]:  # Utilisateur ajouté au groupe
                    all_menus = self.env['ir.ui.menu'].search([])
                    menus_to_hide = all_menus.filtered(
                        lambda menu: menu.id not in [menu_my_vehicles.id, menu_my_pieces.id]
                    )
                    user.hide_menu_access_ids = [(6, 0, menus_to_hide.ids)]
                    self._assigned_multi_company_mecano()            
                else:  # Utilisateur retiré du groupe
                    user.hide_menu_access_ids = [(5,)]


    def _assigned_multi_company_mecano(self):
        companies = self.env['res.company'].search([
                ('name', 'in', ['Ocean Trade', 'Continental Auto'])
            ])
        if companies:
            for user in self:
                user.write({
                    'company_ids': [(4, cid) for cid in companies.ids if cid not in user.company_ids.ids]
                })