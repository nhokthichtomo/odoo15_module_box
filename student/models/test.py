from odoo import models, fields, api

class Test2(models.Model):
    _name = 'test2'

    number = fields.Integer()
    after = fields.Integer(compute='_compute_acount', store=True)

    @api.depends('number')
    def _compute_acount(self):
        for r in self:
            r.after = r.number * 2

    def refresh(self):
    # self.env[test2].flush_model()
        for r in self:
            r.number = 40
        a = self.env.cr.execute("""
        select * from test2
        """)
        print(self.env.cr.fetchall())

        self.env.flush_all()

        a = self.env.cr.execute("""
        select * from test2
        """)
        print(self.env.cr.fetchall())

    @api.model
    def create(self, vals):
        a = self.env.cr.execute("""
        select * from test2
        """)
        print(self.env.cr.fetchall())

        record = super(Test2, self).create(vals)

        a = self.env.cr.execute("""
            select * from test2
            """)
        print(self.env.cr.fetchall())

        return record

    def up_number(self):
        all = self.env['test2'].search([])
        for r in all:
            r.number = r.number + 1