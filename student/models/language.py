from odoo import models, fields

class Language(models.Model):
    _name = 'language'
    _description = 'Language'

    name = fields.Char(string='Name', required=True)
    level = fields.Selection([('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],string='Level',required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),    
        ('valid_level', 'CHECK(level IN (\'beginner\', \'intermediate\', \'advanced\'))', 'Invalid level'),
    ]