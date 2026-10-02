from odoo import models, fields


class BloomDevice(models.Model):
    _name = 'bloom.device'
    _description = 'Bloom Device'
    _order = 'name'

    name = fields.Char(string='Device Name', required=True)
    serial_number = fields.Char(string='Serial Number')
    category = fields.Char(string='Category')
    status = fields.Selection(
        [
            ('available', 'Available'),
            ('in_use', 'In Use'),
            ('maintenance', 'Maintenance'),
        ],
        string='Status',
        required=True,
        default='available',
    )
    team_id = fields.Many2one('bloom.team', string='Assigned To', ondelete='set null')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')
