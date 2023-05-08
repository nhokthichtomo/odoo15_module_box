from xml.dom import ValidationErr
from odoo import models, fields, api

class StudentTest(models.Model):
    _name = 'student.test'
    _description = 'Student test'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    code = fields.Integer(string='Code', required=True)
    address = fields.Text(string='Address')
    ranking = fields.Selection(selection=[('very good', 'Very Good'), ('good', 'Good'), ('average', 'Average'), ('weak', 'Weak')],string='Ranking')
    has_experience = fields.Boolean(string='Has Experience', default=False)
    avatar = fields.Binary(string='Avatar')
    introduce = fields.Html(string='Introduce')
    logo = fields.Image(string='Logo', max_width=128, max_height=128)
    currency_id = fields.Many2one('res.currency', string='Currency')
    class_fund = fields.Monetary(string='Class Fund', currency_field='currency_id')
    date_of_birth = fields.Date(string='Date of birth')
    attendance_time_start = fields.Datetime(string='Attendance time start')
    order_lines = fields.One2many('sale.order.line', 'order_id', string='Order Lines')
    total_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    project_id = fields.Many2one('project.project', string='Project')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),
        ('positive_age', 'CHECK(age >= 0)', 'Age must be positive'),
        ('valid_gender', 'CHECK(gender IN (\'male\', \'female\'))', 'Gender must be Male or Female'),
        ('valid_ranking', 'CHECK(ranking IN(\'very good\', \'good\', \'average\', \'weak\'))', 'Ranking must be very good, good, average or weak'),
    ]
    
    @api.depends('age', 'ranking')
    def _compute_total_score(self):
        for record in self:
            total = record.age * 10
            if record.ranking == 'very good':
                total *= 1.5
            elif record.ranking == 'good':
                total *= 1.2
            elif record.ranking == 'average':
                total *= 1
            else:
                total *= 0.8
            record.total_score = total
    
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 0 or record.age > 120:
                raise ValidationErr('Age must be between 0 and 120')
    
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 0:
            self.age = 0
        elif self.age > 100:
            self.age = 100

    @api.model
    def create(self, vals):
        # Perform some custom logic before creating a new record
        return super(StudentTest, self).create(vals)        
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(StudentTest, self).create(vals_list)
        # Perform some custom logic after creating the new records
        return records

class SaleOrder(models.Model):
    _name = 'sale.order.line'
    _description = 'Sale Order Line'

    order_id = fields.Many2one('student.test', string='Order Id')   
    quantity = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    price_total = fields.Float(string='Total Price', compute='_compute_total_price')

    @api.depends('quantity', 'price_unit')
    def _compute_total_price(self):
        for line in self:
            line.price_total = line.quantity * line.price_unit   

    @api.onchange('quantity', 'price_unit')
    def _compute_total_price(self):
        for record in self:
            record.price_total = record.quantity * record.price_unit
            
    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationErr("Quantity cannot be negative")
            
    @api.model
    def create(self, vals):
        # Perform some custom logic before creating a new record
        return super(SaleOrder, self).create(vals)        
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(SaleOrder, self).create(vals_list)
        # Perform some custom logic after creating the new records
        return records