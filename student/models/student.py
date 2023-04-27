from odoo import models, fields

class Student(models.Model):
    _name = 'student'
    _description = 'Student'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    code = fields.Integer(string='Code', required=True)
    address = fields.Text(string='Address')
    ranking = fields.Selection(selection=[('very good', 'Very Good'), ('good', 'Good'), ('average', 'Average'), ('weak', 'Weak')],string='Ranking')
    has_experience = fields.Boolean(string='Has Experience', default=False)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),
        ('positive_age', 'CHECK(age >= 0)', 'Age must be positive'),
        ('valid_gender', 'CHECK(gender IN (\'male\', \'female\'))', 'Gender must be Male or Female'),
        ('valid_rankink', 'CHECK(ranking IN(\'very good\', \'good\', \'average\', \'weak\'))', 'Ranking must be very good, good, average or weak'),
    ]

