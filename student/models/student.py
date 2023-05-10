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
    
    @api.depends_context('email')
    def _compute_email(self):   #tính toán giá trị của trường email dựa trên giá trị của context email
        #Khi có sự thay đổi về giá trị của context email, Odoo sẽ tự động tính toán lại giá trị của trường email bằng cách gọi phương thức _compute_email.
        if self.env.context.get('email'):
            self.email = self.env.context['email']
        else:
            self.email = ''
            
   
    @api.constrains('score')
    def _check_score(self):
        #kiểm tra giá trị của trường score trên model
        for record in self:
            if record.score < 0 or record.score > 4:
                raise ValidationError('Age must be between 0 and 4')            
    
            
    @api.onchange('age')
    def _onchange_age(self):
        #kiểm tra giá trị của trường age trên model
        if self.age < 0:
            self.age = 0
        elif self.age > 100:
            self.age = 100    
                
    
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if record.code < 0:
                raise ValidationError('Code must be positive')
            
    @api.model_create_multi
    #tạo nhiều bản ghi cùng một lúc
    def create(self, vals_list):    #(đại diện cho model hiện tại, danh sách các dict, mỗi dict chứa thông tin cho một bản ghi mới)
        #tạo nhiều bản ghi mới với thông tin được chỉ định trong các dict trong vals_list
        records = super(Student, self).create(vals_list)
        #trả về danh sách các bản ghi được tạo mới
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
    
    
    # @api.model
    # def copy(self, default=None):
    #     #dict default mới, chuyển tham số default vào hoặc tạo ra một dict rỗng nếu default là None
    #     default = dict(default or {})
    #     #thêm một giá trị cho trường name trong dict default
    #     default.update({'name': 'Copy of %s' % (self.name)})
    #     #Tạo ra một bản sao của đối tượng hiện tại
    #     return super(Student, self).copy(default)
    
    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     #tìm kiếm các bản ghi thỏa mãn các điều kiện tìm kiếm được chỉ định.
    #     records = self.env['student'].search(args, offset=offset, limit=limit, order=order, count=count)
    #     #trả về danh sách các bản ghi thỏa mãn các điều kiện tìm kiếm
    #     return records
    
    @api.model
    # tải trước thông tin của trường name cho tất cả các bản ghi trong model
    def prefetch_name(self):
        # tìm kiếm tất cả các bản ghi trong model
        students = self.search([])
        students.prefetch(['name'])
    
    @api.model
    # truy xuất giá trị được lưu trữ trong bộ nhớ cache 
    def _get_cached_value(self, key): 
        # truy cập đối tượng cache, gọi phương thức get với tham số là key cần truy xuất       
        return self.env.cache.get(key)

    @api.model
    # lưu trữ giá trị vào bộ nhớ cache
    def _set_cached_value(self, key, value): 
        # truy cập đối tượng cache, gọi phương thức set với tham số là key và value cần lưu trữ        
        self.env.cache.set(key, value)

    @api.model
    def get_all_students(self):
        key = 'all_students'
        # phương thức get của đối tượng cache để truy xuất thông tin của tất cả các student từ bộ nhớ cache
        students = self.env.cache.get(key)
        if students is None:
            # tìm kiếm tất cả các bản ghi
            # sau đó đọc thông tin của tất cả các bản ghi này
            students = self.search([]).read()
            # lưu trữ chúng vào bộ nhớ cache bằng cách sử dụng phương thức set của đối tượng cache
            self.env.cache.set(key, students)
        return students
    