from odoo import models, fields


class BloomAppointment(models.Model):
    _name = 'bloom.appointment'
    _description = 'Bloom Appointment'
    _order = 'date desc'

    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    staff_id = fields.Many2one('bloom.staff', string='Assigned Staff')
    date = fields.Datetime(
        string='Appointment Date', required=True, default=fields.Datetime.now
    )
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
