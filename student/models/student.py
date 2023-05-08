from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Student(models.Model):
    _name = 'student'    
    _description = 'Extend student model'

    name = fields.Char(string='Name', required=True)    #(required=True : gia tri bat buoc)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    code = fields.Integer(string='Code', required=True)
    address = fields.Text(string='Address')
    ranking = fields.Selection(selection=[('very good', 'Very Good'), ('good', 'Good'), ('average', 'Average'), ('weak', 'Weak')],string='Ranking')
    has_experience = fields.Boolean(string='Has Experience', default=False)     
    city = fields.Text(string='City')
    introduce = fields.Html(string='Introduce')
    date_of_birth = fields.Date(string='Date of birth')
    attendance_time_start = fields.Datetime(string='Attendance time start')
    email = fields.Char(string='Email', required=True)
    score = fields.Float(String='Score')
    total_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)
    logo = fields.Image(string='Logo', max_width=128, max_height=128)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    project_id = fields.Many2one('project.project', string='Project')
    
    _sql_constraints = [        
        ('unique_name', 'unique(name)', 'The name must be unique'),
        ('positive_age', 'CHECK(age >= 0)', 'Age must be positive'),
        ('valid_gender', 'CHECK(gender IN (\'male\', \'female\'))', 'Gender must be Male or Female'),
        ('valid_ranking', 'CHECK(ranking IN(\'very good\', \'good\', \'average\', \'weak\'))', 'Ranking must be very good, good, average or weak'),
        ('valid_has_experience', 'CHECK(has_experience IN (True, False))', 'Has Experience must be True or False'),
        ('valid_city', 'CHECK(city!= \'\')', 'City must not be empty'),
        ('valid_introduce', 'CHECK(introduce!= \'\')', 'Introduce must not be empty'),
        ('valid_date_of_birth', 'CHECK(date_of_birth!= \'\')', 'Date of birth must not be empty'),
        ('valid_attendance_time_start', 'CHECK(attendance_time_start!= \'\')', 'Attendance time start must not be empty'),
        ('valid_email', 'CHECK(email!= \'\')', 'Email must not be empty'),
        ('valid_score', 'CHECK(score >= 0)', 'Score must be positive'),
        ('valid_total_score', 'CHECK(total_score >= 0)', 'Total score must be positive'),
        ('valid_code', 'CHECK(code >= 0)', 'Code must be positive'),
        ('valid_address', 'CHECK(address!= \'\')', 'Address must not be empty'),        
    ]
    
    
    @api.depends('score', 'ranking')    
    def _compute_total_score(self):
        for record in self:
            total = record.score * 1
            if record.ranking == 'very good':
                total >= 3.2
            elif record.ranking == 'good':
                total >= 2.5
            elif record.ranking == 'average':
                total >= 2.0
            else:
                total >= 0.8
            record.total_score = total
    
    @api.depends_context('score')
    def _compute_score(self):
        for record in self:
            record.score = record.score / record.total_score
            
            
   
    @api.constrains('score')
    def _check_score(self):
        for record in self:
            if record.score < 0 or record.score > 4:
                raise ValidationError('Age must be between 0 and 4')
            
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 0 or record.age > 100:
                raise ValidationError('Age must be between 0 and 100')
            
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 0:
            self.age = 0
        elif self.age > 100:
            self.age = 100
    
    @api.onchange('score')
    def _onchange_score(self):
        if self.score < 0 or self.score > 4:
            self.score = 0            
    
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if record.code < 0:
                raise ValidationError('Code must be positive')
            

    @api.model
    def create(self, vals):
        # Perform some custom logic before creating a new record
        return super(Student, self).create(vals)
    
    @api.model
    def write(self, vals):
        # Perform some custom logic before updating a record
        return super(Student, self).write(vals)
    
    
    
    @api.model
    def unlink_group(self):
        # Perform some custom logic before deleting a record
        return super(Student, self).unlink_group()        
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(Student, self).create(vals_list)
        # Perform some custom logic after creating the new records
        return records
    
    @api.model
    def add_user_to_group(self, user_id, group_id):
        # Lấy đối tượng người dùng và nhóm từ ID
        user = self.env['res.users'].browse(user_id)
        group = self.env['res.groups'].browse(group_id)
        # Kiểm tra xem người dùng đã có trong nhóm chưa
        if group.id not in user.groups_id.ids:
            # Thêm nhóm vào danh sách nhóm của người dùng
            user.write({'groups_id': [(4, group.id)]})
    
    

