from odoo import fields, models


class WeeklyScheduleWizard(models.TransientModel):
    _name = "hospital.weekly.schedule.wizard"
    _description = "Weekly Schedule Wizard"

    week_type = fields.Selection(
        [("even", "Even Weeks"), ("odd", "Odd Weeks")],
        string="Week Type",
        required=True,
    )
    doctor_schedule_ids = fields.One2many(
        "hospital.doctor.schedule", "id", string="Schedules"
    )

    def apply_schedules(self):
        for schedule in self.doctor_schedule_ids:
            self.env["hospital.doctor.schedule"].create(
                {
                    "doctor_id": schedule.doctor_id.id,
                    "schedule_date": schedule.schedule_date,
                    "start_time": schedule.start_time,
                    "end_time": schedule.end_time,
                }
            )
