from odoo import models, fields

class City(models.Model):
    _name = 'city'
    _description = 'City'

    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('my_module.country', string='Country', required=True)

    _sql_constraints = [
        ('unique_name_country', 'unique(name, country_id)', 'Name must be unique within the country')
    ]