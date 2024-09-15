from odoo import fields, models


class Disease(models.Model):
    _name = "hospital.disease"
    _description = "Disease"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one("hospital.disease", string="Parent category")
    child_ids = fields.One2many("hospital.disease", "parent_id", string="Subcategories")
