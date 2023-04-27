from odoo import models, fields

class Countryside(models.Model):
    _name = 'countryside'
    _description = 'Countryside'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    province_id = fields.Many2one('my_module.province', string='Province', required=True)

    _sql_constraints = [
        ('unique_code_province', 'unique(code, province_id)', 'Code must be unique within the province')
    ]