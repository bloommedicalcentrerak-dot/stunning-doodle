from odoo import models, fields


class BloomService(models.Model):
    _name = 'bloom.service'
    _description = 'Bloom Clinic Service'
    _order = 'service_type, name'

    name = fields.Char(string='Service', required=True)
    service_type = fields.Selection(
        [
            ('consultation', 'Consultation'),
            ('laser', 'Laser'),
            ('slimming', 'Slimming'),
            ('derma', 'Dermatology'),
            ('dental', 'Dental'),
            ('massage', 'Massage'),
            ('beauty', 'Beauty'),
            ('pain', 'Pain Therapy'),
            ('other', 'Other'),
        ],
        string='Service Type',
        required=True,
        default='consultation',
    )
    price = fields.Float(string='Price', required=True, default=0.0)
    duration = fields.Float(
        string='Duration (hours)',
        default=0.5,
        help='Default duration used when the service is booked.',
    )
    room_id = fields.Many2one('bloom.room', string='Default Room')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
