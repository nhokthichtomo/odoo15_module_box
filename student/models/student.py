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
    ranking = fields.Selection(selection=[('very good', 'Very Good'), ('good', 'Good'), ('average', 'Average'), ('weak', 'Weak')], string='Ranking', compute='_compute_total_score')
    has_experience = fields.Boolean(string='Has Experience', default=False)     
    city = fields.Text(string='City')
    introduce = fields.Html(string='Introduce')     #lưu trữ đoạn văn bản được định dạng dưới dạng HTML
    date_of_birth = fields.Date(string='Date of birth')
    attendance_time_start = fields.Datetime(string='Attendance time start')
    email = fields.Char(string='Email', required=True)
    score = fields.Float(String='Score')    
    logo = fields.Image(string='Logo', max_width=128, max_height=128)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    project_id = fields.Many2one('project.project', string='Project')   #Many2one được sử dụng để thiết lập mối quan hệ nhiều-một (many-to-one) giữa hai đối tượng
    teacher_id = fields.Many2one('teacher', string='Teacher')
    is_private = fields.Boolean(string='Is Private', groups='base.studen_group_admin')
    
    _sql_constraints = [        
        ('unique_name', 'unique(name)', 'The name must be unique'),     #yêu cầu giá trị trong trường phải là duy nhất
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
        ('valid_code', 'CHECK(code >= 0)', 'Code must be positive'),
        ('valid_address', 'CHECK(address!= \'\')', 'Address must not be empty'),        
    ]
            
    @api.depends('score')    
    def _compute_total_score(self):
        for record in self:
            if record.score >= 3.3:
                record.ranking = 'very_good'
            elif record.score >= 2.5:
                record.ranking = 'good'
            elif record.score >= 1.5:
                record.ranking = 'average'
            else:
                record.ranking = 'weak'            
    
    @api.depends_context('language')
    def _compute_name(self):
        for student in self:
            if student.name_en and student.name_vi:
                if self.env.context.get('language') == 'vi_VI':
                    student.name = student.name_vi
                else:
                    student.name = student.name_en
            else:
                student.name = student.name_en or student.name_vi            
            
   
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
    
    
    @api.model
    def copy(self, vals=None):
        new_student = Student(self.name, self.age)
        if vals:
            # update any additional properties based on vals
            pass
        return new_student
    
    @api.model
    def copy_data(self, default=None):
        new_defaults = {'title': ("%s (copy)") % (self.title)}
        default = dict(new_defaults, **(default or {}))
        return super(Student, self).copy_data(default)
    
    @api.model
    def get_student_info(self):        #được sử dụng để lấy tất cả sinh viên và tên giáo viên tương ứng của họ
        students = self.env['student'].search([])
        # prefetch() để tải trước trường teacher_id cho tất cả sinh viên. 
        # Sau đó, chúng ta truy xuất tên giáo viên bằng cách sử dụng trường teacher_id.name mà không cần phải tải trường teacher_id mỗi lần truy xuất.
        students.prefetch(['teacher_id'])
        result = []
        for student in students:
            result.append({
                'name': student.name,
                'age': student.age,
                'score': student.score,
                'teacher_name': student.teacher_id.name,
            })
        return result
    
    @api.model
    def _get_cached_value(self, key):        
        return self.env.cache.get(key)

    @api.model
    def _set_cached_value(self, key, value):        
        self.env.cache.set(key, value)

    @api.model
    def get_average_score(self):
        
        cache_key = 'student_average_score'
        cached_value = self._get_cached_value(cache_key)
        if cached_value:
            return cached_value

        # If the value is not in the cache, compute it and store it in the cache
        students = self.env['student'].search([])
        total_score = sum(student.score for student in students)
        average_score = total_score / len(students) if students else 0.0
        self._set_cached_value(cache_key, average_score)
        return average_score
    