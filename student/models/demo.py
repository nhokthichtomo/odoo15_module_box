from odoo import models, fields, api   

class Student(models.Model):
    _name = 'student'    
    _description = 'Extend student model'
    
    @api.model
    def default_get(self, fields):
        defaults = super(Student, self).default_get(fields)
        defaults['age'] = 23
        defaults['gender'] ='male'        
        defaults['code'] = 1
        defaults['score'] = 10.0
        defaults['total_score'] = 10.0
        defaults['ranking'] = 'average'
        defaults['has_experience'] = False
        defaults['city'] = ''
        return defaults
        
    def name_create(cls, name):
        record = cls.create({'name': name})
        return record.name_get()[0]
    
    def write(self, vals):
        res = super(Student, self).write(vals)
        # Thực hiện các thao tác khác nếu cần
        return   
    
    def browse(cls, id):
        record = cls.env['student'].search([('id', '=', id)], limit=1)
        return record
        
   
        
    def read(self, fields=None, load='_classic_read'):
        values = super(Student, self).read(fields=fields, load=load)
        return values
        
    def read_group(cls, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        records = cls.env['student'].search(domain, offset=offset, limit=limit, order=orderby)
        grouped_data = records.read_group(fields, groupby, lazy=lazy)
        return grouped_data
    
    def unlink(self):
        student = Student() # create a student object
        student.delete(self) # delete the object from the database
        student.commit() # commit the changes
        student.close() # close the student
        
    def update(self, values):
        self.write(values)
        self.env.cr.commit()
        
    def ids(cls):
        record_ids = cls.env['student'].search([], order='code').ids
        return record_ids
    
    def ensure_one(student):
        student = Student() # create a student object
        student.ensure_one() # ensure the object exists in the database
        student.commit() # commit the changes
        student.close() # close the student     

    def exists(self):
        record = self.search([('id', '=', self.id)])
        if record:
            return True
        else:
            return False
        
    def exists(self):
        return bool(self.id)
    
    def mapped(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'code': self.code,
            'total_score': self.total_score,
            'ranking': self.ranking,
            'has_experience': self.has_experience,
            'city': self.city,
            'introduce': self.introduce,
            'date_of_birth': self.date_of_birth,
            'attendance_time_start': self.attendance_time_start,
            'email': self.email,
            'address': self.address,
        }
        
    def filtered(cls, domain, order=None, limit=None, offset=None):
        records = cls.env['school'].search(domain, order=order, limit=limit, offset=offset)
        return records
    
    def filtered_domain(cls, domain):
        records = cls.env['school'].search(domain)
        return records
    
    def sorted(cls):
        records = cls.env['school'].sorted()
        return records
    
    def search(cls, domain, offset=0, limit=None, order=None, count=False):
        records = cls.env['school'].search(domain, offset=offset, limit=limit, order=order, count=count)
        return records
        
    def search_count(cls, domain):
        count = cls.env['school'].search_count(domain)
        return count