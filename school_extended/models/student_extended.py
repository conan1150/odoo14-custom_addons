from odoo import fields, models


# class SchoolProfile(models.Model):
#     _name = 'school.profile'


class SchoolStudent(models.Model):
    _inherit = 'school.student'

    student_full_name = fields.Char("Full Name")


