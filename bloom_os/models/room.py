from odoo import models, fields


class BloomRoom(models.Model):
    _name = 'bloom.room'
    _description = 'Bloom Clinic Room'
    _order = 'sequence, name'

    name = fields.Char(string='Room', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    room_type = fields.Selection(
        [
            ('clinic', 'Clinic'),
            ('laser', 'Laser'),
            ('beauty', 'Beauty'),
            ('massage', 'Massage'),
            ('slimming', 'Slimming'),
            ('dental', 'Dental'),
            ('service', 'Service / Support'),
        ],
        string='Room Type',
        required=True,
        default='clinic',
    )
    capacity = fields.Integer(string='Capacity', default=1)
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
