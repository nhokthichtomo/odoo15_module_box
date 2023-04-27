from odoo import models, fields

class FluentLanguage(models.Model):
    _name = 'fluent_language'
    _description = 'Fluent Language'

    name = fields.Char(string='Name', required=True)
    level = fields.Selection([('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],string='Level',required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),    
        ('valid_level', 'CHECK(level IN (\'beginner\', \'intermediate\', \'advanced\'))', 'Invalid level'),
    ]