from odoo import models, fields, api
from datetime import datetime, time, timedelta

class service_product_list(models.Model):
    _inherit = "service.product.list"

    hr_employee_service_ids = fields.One2many("hr_employee.service.product.list.rel",inverse_name="service_product_list_id"
                                              ,string="liste service employe")
    date_start_service = fields.Datetime(string="Date commencement du tache")
    date_end_service = fields.Datetime(string="Date fin du tache")
    technician_display_status = fields.Html(
        string="Etat des techniciens",
        compute='_compute_technician_display'
    )

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

    @api.model
    def _calcule_date_start_end_service(self):
        date_start_service_min = None
        date_end_service_max = None
        all_start_dates = []
        end_dates = []
        for hr_employee_service_id in self.hr_employee_service_ids:
            if hr_employee_service_id.date_start_service:
                all_start_dates.append(hr_employee_service_id.date_start_service)
            if hr_employee_service_id.date_end_service:
                end_dates.append(hr_employee_service_id.date_end_service)
        if len(all_start_dates) == len(self.hr_employee_service_ids):  
            date_start_service_min = min(all_start_dates)
        if len(end_dates) == len(self.hr_employee_service_ids):  
            date_end_service_max = max(end_dates)
        self.date_start_service = date_start_service_min
        self.date_end_service = date_end_service_max

    @api.model
    def _calcule_time_done(self):
        start = self.date_start_service
        end = self.date_end_service or datetime.now()

        if not start and not end:
            return 0
        if not start:
            return 0

        work_start = time(8, 0)
        work_end = time(17, 30)

        def is_work_day(date):
            return date.weekday() < 5  # Monday to Friday

        def compute_work_seconds(start_dt, end_dt):
            total_seconds = 0
            current = start_dt

            while current.date() <= end_dt.date():
                if is_work_day(current):
                    # Define workday range for current date
                    day_start = datetime.combine(current.date(), work_start)
                    day_end = datetime.combine(current.date(), work_end)

                    # Calculate effective start and end for this day
                    effective_start = max(day_start, current)
                    effective_end = min(day_end, end_dt)

                    if effective_start < effective_end:
                        delta = effective_end - effective_start
                        total_seconds += delta.total_seconds()
                current += timedelta(days=1)
                current = datetime.combine(current.date(), time(0, 0))

            return int(total_seconds)
        return compute_work_seconds(start, end)
    @api.model
    def _update_time_done_date_start_end(self):
        self._calcule_date_start_end_service()
        print("nombre hr_employee",len(self.hr_employee_service_ids))
        # time_done = self._calcule_time_done()
        self.write({
            "date_start_service":self.date_start_service,
            "date_end_service":self.date_end_service,
        })

    