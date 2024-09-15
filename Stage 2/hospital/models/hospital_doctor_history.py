from odoo import api, fields, models


class DoctorHistory(models.Model):
    _name = "hospital.doctor.history"
    _description = "Doctor History"

    name = fields.Char(string="Doctor Visit", compute="_compute_name", store=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    assignment_date = fields.Date(required=True)

    @api.depends("patient_id", "doctor_id", "assignment_date")
    def _compute_name(self):
        for record in self:
            if record.patient_id and record.doctor_id and record.assignment_date:
                record.name = f"{record.patient_id.name} - {record.doctor_id.name} - {record.assignment_date}"
            else:
                record.name = "New Doctor History"
