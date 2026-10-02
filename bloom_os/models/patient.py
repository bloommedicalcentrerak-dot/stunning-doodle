from odoo import api, fields, models


class BloomPatient(models.Model):
    _name = 'bloom.patient'
    _description = 'Bloom Patient'
    _order = 'name'

    name = fields.Char(string='Patient Name', required=True)
    phone = fields.Char(string='Phone')
    emirates_id = fields.Char(string='Emirates ID')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    appointment_count = fields.Integer(
        string='Appointments', compute='_compute_record_counts'
    )
    laser_count = fields.Integer(
        string='Laser Sessions', compute='_compute_record_counts'
    )
    slimming_count = fields.Integer(
        string='Slimming Sessions', compute='_compute_record_counts'
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

    @api.depends('appointment_ids', 'laser_ids', 'slimming_ids')
    def _compute_record_counts(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)
            rec.laser_count = len(rec.laser_ids)
            rec.slimming_count = len(rec.slimming_ids)
