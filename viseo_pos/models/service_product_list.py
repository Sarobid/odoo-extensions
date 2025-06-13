from odoo import models, fields, api
from datetime import datetime, time, timedelta

class service_product_list(models.Model):
    _inherit = "service.product.list"

    hr_employee_service_ids = fields.One2many("hr_employee.service.product.list.rel",inverse_name="service_product_list_id"
                                              ,string="liste service employe")
    technician_display_status = fields.Html(
        string="Etat des techniciens",
        compute='_compute_technician_display'
    )
    time_past_display = fields.Char(string="Temps passée",compute='_compute_time_past_display')

    @api.depends("hr_employee_service_ids")
    def _compute_time_past_display(self):
        for rec in self:
            tmps = 0
            rec.time_past_display = ""
            print(rec.ids)
            print("tmps", tmps)
            print("rec.hr_employee_service_ids",len(rec.hr_employee_service_ids))
            all_intervall_travail = []
            for hr_employee_service_id in rec.hr_employee_service_ids:
                value_travail = hr_employee_service_id._get_heure_travail()
                all_intervall_travail = all_intervall_travail + value_travail
            all_intervall_travail = self.trier_par_diff_decroissant(all_intervall_travail)
            resultat = self.trouver_intersections(all_intervall_travail)
            tmps = sum(intervalle["diff"] for intervalle in resultat)
            rec.time_past_display = self.tmp_to_format_horodata(tmps)

    def tmp_to_format_horodata(self,tmps):
        total_seconds = int(tmps)
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_past_display = ""
        if days > 0:
            time_past_display += f"{days}j{'' if days > 1 else ''} "
        if hours > 0:
            time_past_display += f"{hours}h{'' if hours > 1 else ''} "
        if minutes > 0:
            time_past_display += f"{minutes}min{'' if minutes > 1 else ''} "
        if seconds > 0 or (
                days == 0 and hours == 0 and minutes == 0):
            time_past_display += f"{seconds}s{'' if seconds > 1 else ''}"
        return time_past_display.strip()

    # Trie par date start décroissante
    def trier_par_diff_decroissant(self,liste_intervalles):
        return sorted(liste_intervalles, key=lambda x: x["start"], reverse=True)

    def trouver_intersections(self,liste, intersections=None, indice=0):
        if intersections is None:
            intersections = []
        if len(liste) <= indice:
            return intersections
        else:
            est_intersect = False
            i = 0
            interTraite = liste[indice]
            while i < len(intersections):
                intervalle = intersections[i]
                if interTraite["start"] <= intervalle["end"] and intervalle["start"] <= interTraite["end"]:
                    intersection_start = min(interTraite["start"], intervalle["start"])
                    intersection_end = max(intervalle["end"], interTraite["end"])
                    diff_seconds = (intersection_end - intersection_start).total_seconds()
                    intersections[i]["start"] = intersection_start
                    intersections[i]["end"] = intersection_end
                    intersections[i]["diff"] = diff_seconds
                    est_intersect = True
                    break
                i += 1
            if not est_intersect:
                intersections.append(interTraite)
            return self.trouver_intersections(liste, intersections, indice + 1)

    @api.depends('hr_employee_service_ids', 'technician')
    def _compute_technician_display(self):
        for rec in self:
            html = "<div style='line-height: 1.6;'>"
            tech_id_order = rec.technician.ids
            sorted_techs = sorted(
                rec.hr_employee_service_ids,
                key=lambda t: tech_id_order.index(t.hr_employee_id.id) if t.hr_employee_id.id in tech_id_order else 9999
            )
            for tech in sorted_techs:
                color = "green"
                follow_state = tech.get_follow_state()
                color = follow_state['color']
                status = follow_state['status']
                html += (
                    f"<div style='margin-bottom: 4px;'>"
                    f"  <span style='"
                    f"      background-color: {color};"
                    f"      color: white;"
                    f"      padding: 2px 6px;"
                    f"      border-radius: 6px;"
                    f"      font-size: 12px;"
                    f"      margin-right: 6px;"
                    f"  '>{status}</span>"
                    f"  <span class='technician-name' style='font-weight: bold;'>{tech.hr_employee_id.name}</span>"
                    f"</div>"
                )
                html += "</div>"
            rec.technician_display_status = html

    