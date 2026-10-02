from odoo import models, fields, api


class BloomPatient(models.Model):
    _name = 'bloom.patient'
    _description = 'Bloom Patient'
    _order = 'name'

    name = fields.Char(string='Patient Name', required=True)
    phone = fields.Char(string='Phone')
    emirates_id = fields.Char(string='Emirates ID')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    general_consent_given = fields.Boolean(
        string='General Consent Form Signed',
        help='Confirms the patient signed the clinic\'s general consent form.',
    )
    consent_signature = fields.Binary(string='Consent Signature')
    referral_source = fields.Char(
        string='Referral Source',
        help='How the patient was referred to the clinic (applies across all departments).',
    )
    follow_up_date = fields.Date(string='Follow-up Date')
    cross_sell_notes = fields.Text(
        string='Cross-selling Notes',
        help='Notes on other services/departments this patient may be interested in.',
    )

    appointment_ids = fields.One2many(
        'bloom.appointment', 'patient_id', string='Appointments'
    )
    laser_ids = fields.One2many(
        'bloom.laser', 'patient_id', string='Laser Sessions'
    )
    slimming_ids = fields.One2many(
        'bloom.slimming', 'patient_id', string='Slimming Sessions'
    )
    consultation_ids = fields.One2many(
        'bloom.consultation', 'patient_id', string='Consultations'
    )
    next_appointment_id = fields.Many2one(
        'bloom.appointment', string='Next Appointment',
        compute='_compute_next_appointment',
    )

    @api.depends(
        'appointment_ids.date', 'appointment_ids.state'
    )
    def _compute_next_appointment(self):
        now = fields.Datetime.now()
        for patient in self:
            upcoming = patient.appointment_ids.filtered(
                lambda appt: appt.state in ('draft', 'confirmed') and appt.date >= now
            ).sorted('date')
            patient.next_appointment_id = upcoming[:1]
