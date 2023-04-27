from odoo import models, fields

class Student(models.Model):
    _name = 'student'
    _description = 'Student'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    id = fields.Integer(string='Id', required=True)
    address = fields.Text(string='Address')
    score = fields.Float(string='Score')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),
        ('positive_age', 'CHECK(age >= 0)', 'Age must be positive'),
        ('valid_gender', 'CHECK(gender IN (\'male\', \'female\'))', 'Gender must be Male or Female'),
        ('valid_score', 'CHECK(score >= 0 AND score <= 10)', 'Score must be between 0 and 10')
    ]

