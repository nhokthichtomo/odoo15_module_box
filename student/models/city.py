from odoo import models, fields

class City(models.Model):
    _name = "city"
    _description = 'City'

    name = fields.Char(string='Name', required=True)
    code = fields.Integer(string='Code', required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique within the country')        
    ]