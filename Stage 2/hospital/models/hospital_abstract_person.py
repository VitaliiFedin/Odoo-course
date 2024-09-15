from odoo import fields, models


class Person(models.AbstractModel):
    _name = "hospital.abstract_person"
    _description = "Abstract Model for Person"

    name = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    gender = fields.Selection([("male", "Male"), ("female", "Female")], required=True)
    photo = fields.Binary()
