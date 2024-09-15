from odoo import fields, models


class ResearchType(models.Model):
    _name = "hospital.research.type"
    _description = "Research Type"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one("hospital.research.type", string="Parent category")
    child_ids = fields.One2many(
        "hospital.research.type", "parent_id", string="Subcategories"
    )


class SampleType(models.Model):
    _name = "hospital.sample.type"
    _description = "Sample Type"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")


class Research(models.Model):
    _name = "hospital.research"
    _description = "Research"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    research_type_id = fields.Many2one(
        "hospital.research.type", string="Type of research", required=True
    )
    doctor_id = fields.Many2one(
        "hospital.doctor", string="The prescribing physician", required=True
    )
    sample_type_id = fields.Many2one("hospital.sample.type", string="Sample type")
    conclusions = fields.Text(string="Conclusions")
    visit_id = fields.Many2one("hospital.doctor.visit", string="Visit")
    diagnosis_id = fields.Many2one("hospital.diagnosis", string="Diagnosis")
