from odoo import models, fields


class BloomRoom(models.Model):
    _name = 'bloom.room'
    _description = 'Bloom Room'
    _order = 'name'

    name = fields.Char(string='Room Name', required=True)
    department_id = fields.Many2one('bloom.department', string='Department')
    active = fields.Boolean(string='Active', default=True)
