from odoo import models, fields

class BloomLaser(models.Model):
    _name = 'bloom.laser'
    _description = 'Bloom Laser Session'

    patient_id = fields.Many2one('bloom.patient', string='Patient')
    session_date = fields.Datetime(string='Session Date')
    area = fields.Char(string='Treatment Area')
    machine = fields.Char(string='Machine Used')
    notes = fields.Text(string='Notes')
