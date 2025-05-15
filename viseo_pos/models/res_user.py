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

    def _restrict_menus_if_in_group(self,vals):
        group_my_vehicles = self.env.ref('viseo_pos.group_rma_vehicle_mecano')
        menu_my_vehicles = self.env.ref('viseo_pos.menu_my_vehicles_root')
        # print("_restrict_menus_if_in_group")
        if group_my_vehicles :
            # print("group_my_vehicles")
            ingroup = 'in_group_'+str(group_my_vehicles.id)
            if ingroup in vals and vals[ingroup] is True:
                # print("assigner in group_rma_vehicle_mecano")
                all_menus = self.env['ir.ui.menu'].search([])
                menu_ids_to_hide = all_menus.filtered(lambda menu: menu.id != menu_my_vehicles.id)
                print(all_menus)
                self.write({
                    'hide_menu_access_ids': [(6, 0, menu_ids_to_hide.ids)]
                })
            # if ingroup in vals and vals[ingroup] is False:
            #     print("nonassigner in group_rma_vehicle_mecano")