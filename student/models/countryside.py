from odoo import models, fields

class Countryside(models.Model):
    _name = 'countryside'
    _description = 'Countryside'

    name = fields.Char(string='Name', required=True)
    code = fields.Integer(string='Code', required=True)
    province = fields.Text(string='Province', required=True)

    _sql_constraints = [        
        ('unique_name', 'unique(name)', 'Name must be unique') 
    ]