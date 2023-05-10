from odoo import models, fields, api


import logging
_logger = logging.getLogger(__name__)

class UpdateWizard(models.TransientModel):
    _name = "student.update.wizard"
    _description = "Update for student model"
    
    name = fields.Char(string='Name')    #(required=True : gia tri bat buoc)
    age = fields.Integer(string='Age')
    date_of_birth = fields.Date(string='Date of birth')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', default='false')
    code = fields.Integer(string='Code')    
    address = fields.Text(string='Address')    
    has_experience = fields.Boolean(string='Has Experience', default=False)
    city = fields.Text(string='City')
    introduce = fields.Html(string='Introduce')
    attendance_time_start = fields.Datetime(string='Attendance time start')
    email = fields.Char(string='Email')
    score = fields.Float(String='Score')    
    logo = fields.Image(string='Logo', max_width=128, max_height=128)    
    
    
    def multi_update(self):
        ids = self.env.context['active_ids'] # selected record ids
        student = self.env["student"].browse(ids)
        new_data = {}
        
        if self.name:
            new_data["name"] = self.name
        if self.age:
            new_data["age"] = self.age
        if self.date_of_birth:
            new_data["date_of_birth"] = self.date_of_birth
        if self.gender:
            new_data["gender"] = self.gender
        if self.code:
            new_data["code"] = self.code
        if self.address:
            new_data["address"] = self.address        
        if self.has_experience:
            new_data["has_experience"] = self.has_experience
        if self.city:
            new_data["city"] = self.city
        if self.introduce:
            new_data["introduce"] = self.introduce
        if self.attendance_time_start:
            new_data["attendance_time_start"] = self.attendance_time_start
        if self.email:
            new_data["email"] = self.email
        if self.score:
            new_data["score"] = self.score        
        if self.logo:
            new_data["logo"] = self.logo
               
        
        student.write(new_data)
        return True
    
    
        