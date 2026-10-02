from odoo import models, fields


class BloomDoctor(models.Model):
    _name = 'bloom.doctor'
    _description = 'Bloom Staff Member'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    role = fields.Selection(
        [
            ('doctor', 'Doctor'),
            ('nurse', 'Nurse'),
            ('therapist', 'Therapist'),
            ('technician', 'Technician'),
            ('reception', 'Reception'),
            ('housekeeping', 'Housekeeping'),
        ],
        string='Role',
        required=True,
        default='doctor',
    )
    specialty = fields.Char(string='Specialty')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    room_id = fields.Many2one('bloom.room', string='Default Room')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)

    appointment_ids = fields.One2many(
        'bloom.appointment', 'doctor_id', string='Appointments'
    )
