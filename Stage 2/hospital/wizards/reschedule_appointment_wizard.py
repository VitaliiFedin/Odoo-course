from odoo import api, fields, models


class RescheduleAppointmentWizard(models.TransientModel):
    _name = "hospital.reschedule.appointment.wizard"
    _description = "Reschedule Appointment Wizard"

    new_doctor_id = fields.Many2one("hospital.doctor", string="New Doctor")
    new_visit_datetime = fields.Datetime(string="New Date and Time")

    def apply_rescheduling(self):
        active_id = self.env.context.get("active_id")
        if not active_id:
            return
        visit = self.env["hospital.doctor.visit"].browse(active_id)
        visit.write(
            {
                "doctor_id": (
                    self.new_doctor_id.id if self.new_doctor_id else visit.doctor_id.id
                ),
                "visit_datetime": self.new_visit_datetime or visit.visit_datetime,
            }
        )
