from odoo import models, fields

class Student(models.Model):
    _name = 'student'
    _description = 'Student'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection(selection=[('boy', 'Boy'), ('girl', 'Girl')], string='Gender')
    id = fields.Integer(string='Id', readonly=True)
    address = fields.Char(string='Address')
    score = fields.Float(string='Score')

