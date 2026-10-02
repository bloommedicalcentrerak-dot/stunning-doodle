from odoo import models, fields


class BloomDepartment(models.Model):
    _name = 'bloom.department'
    _description = 'Bloom Department'
    _order = 'name'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active', default=True)
