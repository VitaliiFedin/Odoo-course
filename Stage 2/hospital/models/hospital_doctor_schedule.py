from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DoctorSchedule(models.Model):
    _name = "hospital.doctor.schedule"
    _description = "Doctor Schedule"

    name = fields.Char(string="Doctor Schedule", compute="_compute_name", store=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    schedule_date = fields.Date(string="Date", required=True)
    start_time = fields.Float(required=True)
    end_time = fields.Float(required=True)

    @api.constrains("doctor_id", "schedule_date", "start_time", "end_time")
    def _check_schedule_overlap(self):
        for schedule in self:
            overlapping_schedules = self.search(
                [
                    ("doctor_id", "=", schedule.doctor_id.id),
                    ("schedule_date", "=", schedule.schedule_date),
                    ("id", "!=", schedule.id),
                    "|",
                    "&",
                    ("start_time", "<=", schedule.start_time),
                    ("end_time", ">", schedule.start_time),
                    "&",
                    ("start_time", "<", schedule.end_time),
                    ("end_time", ">=", schedule.end_time),
                ]
            )
            if overlapping_schedules:
                raise ValidationError(
                    "The doctor's schedule overlaps with the existing one."
                )

    @api.depends("doctor_id", "schedule_date")
    def _compute_name(self):
        for record in self:
            if record.doctor_id and record.schedule_date:
                record.name = f"{record.doctor_id.name} - {record.schedule_date}"
            else:
                record.name = "New Doctor Schedule"
