from odoo import models, fields, api


import logging
_logger = logging.getLogger(__name__)

class UpdateWizard(models.TransientModel):
    _name = "student.update.wizard"
    _description = "Update for student model"
    
    date_of_birth = fields.Date(string='Date of birth')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', required=True, default='false')
    code = fields.Integer(string='Code', required=True)    
    address = fields.Text(string='Address')
    

    def multi_update(self):
        ids = self.env.context['active_ids'] # selected record ids
        student = self.env["student"].browse(ids)
        new_data = {}
        
        if self.date_of_birth:
            new_data["date_of_birth"] = self.date_of_birth
        if self.gender:
            new_data["gender"] = self.gender
        if self.code:
            new_data["code"] = self.code        
        if self.address:
            new_data["address"] = self.address        
        
        student.write(new_data)
        return True
    
    
        