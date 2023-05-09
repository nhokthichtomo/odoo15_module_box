from odoo import models, fields, api


import logging
_logger = logging.getLogger(__name__)

class UpdateWizard(models.TransientModel):
    _name = "student.update.wizard"
    _description = "Update for student model"
    
    name = fields.Char(string='Name', required=True)    #(required=True : gia tri bat buoc)
    age = fields.Integer(string='Age', required=True)
    date_of_birth = fields.Date(string='Date of birth')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', required=True, default='false')
    code = fields.Integer(string='Code', required=True)    
    address = fields.Text(string='Address')
    ranking = fields.Selection(selection=[('very good', 'Very Good'), ('good', 'Good'), ('average', 'Average'), ('weak', 'Weak')],string='Ranking')
    has_experience = fields.Boolean(string='Has Experience', default=False)     
    city = fields.Text(string='City')
    introduce = fields.Html(string='Introduce')
    attendance_time_start = fields.Datetime(string='Attendance time start')
    email = fields.Char(string='Email', required=True)
    score = fields.Float(String='Score')
    total_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)
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
        if self.ranking:
            new_data["ranking"] = self.ranking
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
        if self.total_score:
            new_data["total_score"] = self.total_score
        if self.logo:
            new_data["logo"] = self.logo
               
        
        student.write(new_data)
        return True
    
    
        