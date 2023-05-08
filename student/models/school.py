
from odoo import models, fields, api, exceptions

class School(models.Model):
    _name = 'school'
    _description = 'School'

    name = fields.Char(string='name', required=True)
    website = fields.Char(string='Website')
    address = fields.Text(string="Address")
    level = fields.Selection(selection=[('primary ','Primary School'), ('secondary ', 'Secondary School'),
                                            ('high ', 'High School'), ('university', 'University')], string='level', required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique'),
        ('valid_level', 'CHECK(level IN (\'primary\', \'secondary\', \'high\', \'university\'))', 'Level must be Primary School, Secondary School, High School or University')        
    ]
    
    @api.constrains('name')
    def _check_name(self):
        for school in self:
            if school.name == school.name:
                raise exceptions.ValidationError('Name must be unique')
            
    @api.constrains('website')
    def _check_website(self):
        for school in self:
            if school.website == school.website:
                raise exceptions.ValidationError('Website must be unique')
            
    @api.onchange('website')
    def _onchange_website(self):
        if self.website:
            self.website = self.website.replace('http://', '').replace('https://', '')
        
        