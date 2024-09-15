from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DoctorVisit(models.Model):
    _name = "hospital.doctor.visit"
    _description = "Doctor visit"

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    visit_datetime = fields.Datetime(required=True)
    diagnosis_id = fields.Many2one("hospital.diagnosis", string="Diagnosis")
    recommendations = fields.Text()
    visit_completed = fields.Boolean(string="Appointment Completed", default=False)
    research_ids = fields.One2many("hospital.research", "visit_id", string="Research")

    @api.constrains("visit_datetime", "doctor_id")
    def _check_doctor_schedule(self):
        for visit in self:
            conflicting_visits = self.search(
                [
                    ("doctor_id", "=", visit.doctor_id.id),
                    ("visit_datetime", "=", visit.visit_datetime),
                    ("id", "!=", visit.id),
                ]
            )
            if conflicting_visits:
                raise ValidationError(
                    "The doctor already has an appointment for this time."
                )

    def write(self, vals):
        for visit in self:
            if visit.visit_completed:
                protected_fields = ["visit_datetime", "doctor_id", "patient_id"]
                if any(field in vals for field in protected_fields):
                    raise ValidationError(
                        "You cannot change the date, time or doctor for an appointment that has already taken place."
                    )
        return super(DoctorVisit, self).write(vals)

    def unlink(self):
        for visit in self:
            if visit.diagnosis_id:
                raise ValidationError(
                    "You cannot delete an appointment with an established diagnosis."
                )
        return super(DoctorVisit, self).unlink()
