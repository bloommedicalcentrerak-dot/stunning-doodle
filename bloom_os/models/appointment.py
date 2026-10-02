from odoo import models, fields


class BloomAppointment(models.Model):
    _name = 'bloom.appointment'
    _description = 'Bloom Appointment'
    _order = 'date desc'

    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    date = fields.Datetime(string='Appointment Date', required=True)
    doctor_id = fields.Many2one('bloom.doctor', string='Doctor')
    room_id = fields.Many2one('bloom.room', string='Room')
    service_type = fields.Selection(
        [
            ('laser', 'Laser'),
            ('slimming', 'Slimming'),
            ('consultation', 'Consultation'),
        ],
        string='Service Type',
        required=True,
        default='consultation',
    )
    notes = fields.Text(string='Notes')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})
