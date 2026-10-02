from odoo import models, fields

class BloomAppointment(models.Model):
    _name = 'bloom.appointment'
    _description = 'Bloom Appointment'

    patient_id = fields.Many2one('bloom.patient', string='Patient')
    date = fields.Datetime(string='Appointment Date')
    service_type = fields.Selection([
        ('laser', 'Laser'),
        ('slimming', 'Slimming'),
        ('consultation', 'Consultation'),
    ], string='Service Type')
    notes = fields.Text(string='Notes')
