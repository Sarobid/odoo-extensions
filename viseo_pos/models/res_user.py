from odoo import models, api

class res_users(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super(res_users, self).create(vals)
        user._restrict_menus_if_in_group(vals)
        return user

    def write(self, vals):
        res = super(res_users, self).write(vals)
        self._restrict_menus_if_in_group(vals)
        return res

    # def _restrict_menus_if_in_group(self,vals):
    #     group_my_vehicles = self.env.ref('viseo_pos.group_rma_vehicle_mecano')
    #     menu_my_vehicles = self.env.ref('viseo_pos.menu_my_vehicles_root')
    #     menu_my_pieces = self.env.ref('viseo_pos.menu_list_piece_mecano_root')
    #     if group_my_vehicles :
    #         ingroup = 'in_group_'+str(group_my_vehicles.id)
    #         if ingroup in vals and vals[ingroup] is True:
    #             all_menus = self.env['ir.ui.menu'].search([])
    #             menu_ids_to_hide = all_menus.filtered(lambda menu: menu.id != menu_my_vehicles.id and menu.id != menu_my_pieces.id)
    #             print(all_menus)
    #             self.write({
    #                 'hide_menu_access_ids': [(6, 0, menu_ids_to_hide.ids)]
    #             })

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
                else:  # Utilisateur retiré du groupe
                    user.hide_menu_access_ids = [(5,)]


    def _assigned_multi_company_mecano(self):
        companies = self.env['res.company'].search([
            ('name', 'in', ['Ocean Trade', 'Continental Auto'])
        ])        
        if companies:
            # Assigne les sociétés trouvées à l'utilisateur
            self.write({
                'company_ids': [(6, 0, companies.ids)]
            })