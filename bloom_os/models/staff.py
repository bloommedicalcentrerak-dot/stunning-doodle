from odoo import api, fields, models


class BloomStaff(models.Model):
    _name = 'bloom.staff'
    _description = 'Bloom Staff'
    _order = 'role, name'

    name = fields.Char(string='Staff Name', required=True)
    role = fields.Selection(
        [
            ('doctor', 'Doctor'),
            ('laser_technician', 'Laser Technician'),
            ('beauty_specialist', 'Beauty Specialist'),
            ('housekeeping', 'Housekeeping'),
            ('reception', 'Reception'),
            ('other', 'Other'),
        ],
        string='Role',
        required=True,
        default='doctor',
    )
    specialty = fields.Char(string='Specialty / Job Title')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    appointment_ids = fields.One2many(
        'bloom.appointment', 'staff_id', string='Appointments'
    )
    laser_ids = fields.One2many('bloom.laser', 'staff_id', string='Laser Sessions')
    slimming_ids = fields.One2many(
        'bloom.slimming', 'staff_id', string='Slimming Sessions'
    )
    # Shared record-count fields and compute logic with bloom.patient.
    # pylint: disable=duplicate-code
    appointment_count = fields.Integer(
        string='Appointments', compute='_compute_record_counts'
    )
    laser_count = fields.Integer(
        string='Laser Sessions', compute='_compute_record_counts'
    )
    slimming_count = fields.Integer(
        string='Slimming Sessions', compute='_compute_record_counts'
    )

    @api.depends('appointment_ids', 'laser_ids', 'slimming_ids')
    def _compute_record_counts(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)
            rec.laser_count = len(rec.laser_ids)
            rec.slimming_count = len(rec.slimming_ids)
    # pylint: enable=duplicate-code
