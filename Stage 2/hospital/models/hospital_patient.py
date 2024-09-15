from datetime import date

from odoo import api, fields, models


class Patient(models.Model):

    _name = "hospital.patient"
    _inherit = "hospital.abstract_person"
    _description = "Hospital's patient"

    birth_date = fields.Date(required=True)
    age = fields.Integer(compute="_compute_age", store=True)
    passport_info = fields.Char()
    contact_person_id = fields.Many2one("hospital.person", string="Contact Person")
    personal_doctor_id = fields.Many2one("hospital.doctor", string="Personal Doctor")

    @api.depends("birth_date")
    def _compute_age(self):
        for patient in self:
            today = date.today()
            patient.age = (
                today.year
                - patient.birth_date.year
                - (
                    (today.month, today.day)
                    < (patient.birth_date.month, patient.birth_date.day)
                )
            )

    @api.model
    def create(self, vals):
        patient = super(Patient, self).create(vals)
        if patient.personal_doctor_id:
            self.env["hospital.doctor.history"].create(
                {
                    "patient_id": patient.id,
                    "doctor_id": patient.personal_doctor_id.id,
                    "assignment_date": fields.Date.today(),
                }
            )
        return patient

    def write(self, vals):
        if "personal_doctor_id" in vals:
            for patient in self:
                if patient.personal_doctor_id.id != vals["personal_doctor_id"]:
                    self.env["hospital.doctor.history"].create(
                        {
                            "patient_id": patient.id,
                            "doctor_id": vals["personal_doctor_id"],
                            "assignment_date": fields.Date.today(),
                        }
                    )
        return super(Patient, self).write(vals)
