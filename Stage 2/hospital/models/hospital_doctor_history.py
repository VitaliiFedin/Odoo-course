from odoo import fields, models


class DoctorHistory(models.Model):
    _name = "hospital.doctor_history"
    _description = "Doctor History"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    assignment_date = fields.Date(required=True)
