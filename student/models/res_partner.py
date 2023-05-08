from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'student'

    @api.model
    def _create_access_rules(self, vals):
        access_rules = super(ResPartner, self)._create_access_rules(vals)
        sales_group = self.env.ref('student.group_student_sales')
        sales_fields = self.env['ir.model.fields'].search([
            ('model', '=', 'student'),
            ('name', 'in', ['name', 'email'])
        ])
        for rule in access_rules:
            if rule['group'] == sales_group.id:
                rule['fields'] == sales_fields.ids
        return access_rules