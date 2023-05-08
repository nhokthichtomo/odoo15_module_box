from odoo import models, fields, api

class StudentInheritance(models.Model):
    _name = "student.inheritance" 
    _inherit = "student"
    _description = "Student prototype inheritance"

    people = fields.Char(string='People')
    nation = fields.Char(string='Nation')
    fee = fields.Integer(string='Fee', default=0)
    cccd = fields.Integer(string='CCCD', default=0)
    
    _sql_constraints = [
        ('people_uniq', 'unique(people)', 'People must be unique'),
        ('nation_uniq', 'unique(nation)', 'Nation must be unique'),
        ('fee_uniq', 'unique(fee)', 'Fee must be unique'),
        ('cccd_uniq', 'unique(cccd)', 'CCCD must be unique'),        
    ]
    
    @api.constrains('cccd')
    def cccd_uniq(self):
        for record in self:
            if record.cccd == 0:
                return True
        return False
    
    @api.constrains('fee')
    def fee_uniq(self):
        for record in self:
            if record.fee == 0:
                return True
        return False