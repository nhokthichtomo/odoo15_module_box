from odoo import models, fields

class School(models.Model):
    _name = 'school'
    _description = 'School'

    name = fields.Char(string='name', required=True)
    website = fields.Char(string='Website')
    address = fields.Text(string="address")
    level = fields.Selection(selection=[('primary ','Frimary School'), ('secondary ', 'Secondary School'),
                                            ('high ', 'High School'), ('university', 'University')], string='level', required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique'),
        ('valid_level', 'CHECK(level IN (\'primary\', \'secondary\', \'high\', \'university\'))', 'Level must be Primary School, Secondary School, High School or University')        
    ]