from odoo import models, fields


class BloomTeam(models.Model):
    _name = 'bloom.team'
    _description = 'Bloom Team'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    role = fields.Char(string='Role')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')
    device_ids = fields.One2many(
        'bloom.device', 'team_id', string='Assigned Devices'
    )
