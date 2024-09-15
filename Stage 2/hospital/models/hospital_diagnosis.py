from odoo import api, fields, models


class Diagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Diagnosis"

    name = fields.Char(string="Diagnosis Name", compute="_compute_name", store=True)
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

    @api.depends("patient_id", "disease_id", "diagnosis_date")
    def _compute_name(self):
        for record in self:
            if record.patient_id and record.disease_id and record.diagnosis_date:
                record.name = f"{record.patient_id.name} - {record.disease_id.name} - {record.diagnosis_date}"
            else:
                record.name = "New Diagnosis"
