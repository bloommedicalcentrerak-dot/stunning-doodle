from odoo import fields, models


class BloomDepartment(models.Model):
    _name = 'bloom.department'
    _description = 'Bloom Department'
    _order = 'name'

    name = fields.Char(string='Department Name', required=True)
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    purchase_ids = fields.One2many(
        'bloom.purchase', 'department_id', string='Purchase Records'
    )
