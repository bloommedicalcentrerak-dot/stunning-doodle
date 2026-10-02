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
    parameters = fields.Char(string='Device Parameters')
    consent_given = fields.Boolean(
        string='Consent Form Signed',
        help='Confirms the patient signed a consent form before the procedure.',
    )
    consent_signature = fields.Binary(string='Consent Signature')
    post_care_instructions = fields.Text(string='Instructions After Session')
    notes = fields.Text(string='Notes')
