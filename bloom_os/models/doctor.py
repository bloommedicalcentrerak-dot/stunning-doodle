from odoo import models, fields


class BloomDoctor(models.Model):
    _name = 'bloom.doctor'
    _description = 'Bloom Doctor'
    _order = 'name'

    name = fields.Char(string='Doctor Name', required=True)
    specialty = fields.Char(string='Specialty')
    department_id = fields.Many2one('bloom.department', string='Department')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(string='Active', default=True)
