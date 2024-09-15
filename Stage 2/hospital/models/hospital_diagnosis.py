from odoo import api, fields, models


class Diagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Diagnosis"

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    disease_id = fields.Many2one("hospital.disease", string="Disease", required=True)
    treatment = fields.Text()
    diagnosis_date = fields.Date(default=fields.Date.today)
    mentor_comment = fields.Text(string="Mentor's comment")

    @api.model
    def create(self, vals):
        diagnosis = super(Diagnosis, self).create(vals)
        if diagnosis.doctor_id.is_intern:
            diagnosis.mentor_comment = "A mentor's comment is required"
        return diagnosis
