from odoo import models, fields


class BloomSlimming(models.Model):
    _name = 'bloom.slimming'
    _description = 'Bloom Slimming Session'
    _order = 'session_date desc'

    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    session_date = fields.Datetime(string='Session Date', required=True)
    program = fields.Char(string='Program Name', required=True)
    weight = fields.Float(string='Weight')
    measurement = fields.Text(
        string='Measurement / InBody Results',
        help='Body measurements or InBody scan results for this session.',
    )
    consent_given = fields.Boolean(
        string='Consent Form Signed',
        help='Confirms the patient signed a consent form before the procedure.',
    )
    consent_signature = fields.Binary(string='Consent Signature')
    post_care_instructions = fields.Text(string='Instructions After Session')
    notes = fields.Text(string='Notes')
