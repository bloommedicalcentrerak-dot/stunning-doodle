from odoo import models, fields


class BloomSlimming(models.Model):
    _name = 'bloom.slimming'
    _description = 'Bloom Slimming Session'
    _order = 'session_date desc'

    patient_id = fields.Many2one('bloom.patient', string='Patient', required=True)
    staff_id = fields.Many2one('bloom.staff', string='Assigned Staff')
    session_date = fields.Datetime(
        string='Session Date', required=True, default=fields.Datetime.now
    )
    program = fields.Char(string='Program Name', required=True)
    weight = fields.Float(string='Weight', help='Recorded weight during the session.')
    notes = fields.Text(string='Notes')
