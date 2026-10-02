from odoo import models, fields

class BloomSlimming(models.Model):
    _name = 'bloom.slimming'
    _description = 'Bloom Slimming Session'

    patient_id = fields.Many2one('bloom.patient', string='Patient')
    session_date = fields.Datetime(string='Session Date')
    program = fields.Char(string='Program Name')
    weight = fields.Float(string='Weight')
    notes = fields.Text(string='Notes')
