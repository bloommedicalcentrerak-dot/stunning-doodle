from odoo import models, fields


class BloomLaser(models.Model):
    _name = 'bloom.laser'
    _description = 'Bloom Laser Session'
    _order = 'session_date desc'

    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    session_date = fields.Datetime(string='Session Date', required=True)
    area = fields.Char(string='Treatment Area', required=True)
    machine = fields.Char(string='Machine Used')
    notes = fields.Text(string='Notes')
