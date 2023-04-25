# -*- coding: utf-8 -*-

from odoo import models, fields

class box(models.Model):
    _name = 'superbox.box'
    _description = 'Box'

    name = fields.Char(string='Name')
    size = fields.Selection(('big','small'), string="Size")
    type = fields.Char(string="Type")
    quantity = fields.Integer(string="Quantity")
    