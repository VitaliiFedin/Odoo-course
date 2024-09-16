from odoo import api, fields, models


class MassDoctorReassignmentWizard(models.TransientModel):
    _name = "hospital.mass.doctor.reassignment.wizard"
    _description = "Mass Doctor Reassignment Wizard"

    new_doctor_id = fields.Many2one(
        "hospital.doctor", string="New Doctor", required=True
    )

    def apply_reassignment(self):
        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            return
        patients = self.env["hospital.patient"].browse(active_ids)
        for patient in patients:
            patient.write({"personal_doctor_id": self.new_doctor_id.id})
