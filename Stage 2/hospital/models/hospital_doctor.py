from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    _name = "hospital.doctor"
    _description = "Doctor"
    _inherit = "hospital.abstract_person"

    specialty = fields.Char()
    mentor_id = fields.Many2one(
        "hospital.doctor", string="Mentor Doctor", domain=[("is_intern", "=", False)]
    )
    is_intern = fields.Boolean()

    @api.constrains("is_intern", "mentor_id")
    def _check_intern_mentor(self):
        for doctor in self:
            if doctor.is_intern and not doctor.mentor_id:
                raise ValidationError("The intern must have a doctor-mentor.")
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError("A mentor doctor cannot be an intern.")
