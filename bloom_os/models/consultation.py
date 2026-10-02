from odoo import models, fields


class BloomConsultation(models.Model):
    _name = 'bloom.consultation'
    _description = 'Bloom Consultation Form'
    _order = 'date desc'

    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    date = fields.Datetime(string='Consultation Date', required=True)
    body_area = fields.Text(string='Body Chart / Area')
    derma_plan = fields.Text(string='Derma Plan')
    consent_given = fields.Boolean(
        string='Consent Form Signed',
        help='Confirms the patient signed a consent form before the procedure.',
    )
    consent_signature = fields.Binary(string='Consent Signature')
    notes = fields.Text(string='Notes')
