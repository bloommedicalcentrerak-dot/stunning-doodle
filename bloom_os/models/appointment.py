from datetime import timedelta

from odoo import models, fields, api


class BloomAppointment(models.Model):
    _name = 'bloom.appointment'
    _description = 'Bloom Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(
        string='Reference', required=True, copy=False, readonly=True,
        default='New',
    )
    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    doctor_id = fields.Many2one('bloom.doctor', string='Doctor / Staff')
    room_id = fields.Many2one('bloom.room', string='Room')
    service_id = fields.Many2one('bloom.service', string='Service')
    date = fields.Datetime(string='Appointment Date', required=True)
    duration = fields.Float(string='Duration (hours)', default=0.5)
    date_end = fields.Datetime(
        string='End Date', compute='_compute_date_end',
        inverse='_inverse_date_end', store=True,
    )
    price = fields.Float(string='Price')
    service_type = fields.Selection(
        [
            ('consultation', 'Consultation'),
            ('laser', 'Laser'),
            ('slimming', 'Slimming'),
            ('derma', 'Dermatology'),
            ('dental', 'Dental'),
            ('massage', 'Massage'),
            ('beauty', 'Beauty'),
            ('pain', 'Pain Therapy'),
            ('other', 'Other'),
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
        tracking=True,
    )

    @api.depends('date', 'duration')
    def _compute_date_end(self):
        for rec in self:
            if rec.date:
                rec.date_end = rec.date + timedelta(hours=rec.duration or 0.0)
            else:
                rec.date_end = False

    def _inverse_date_end(self):
        for rec in self:
            if rec.date and rec.date_end and rec.date_end > rec.date:
                delta = rec.date_end - rec.date
                rec.duration = delta.total_seconds() / 3600.0

    @api.onchange('service_id')
    def _onchange_service_id(self):
        if not self.service_id:
            return
        self.price = self.service_id.price
        self.duration = self.service_id.duration or self.duration
        if self.service_id.room_id:
            self.room_id = self.service_id.room_id
        allowed = dict(self._fields['service_type'].selection)
        if self.service_id.service_type in allowed:
            self.service_type = self.service_id.service_type

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id.room_id and not self.room_id:
            self.room_id = self.doctor_id.room_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bloom.appointment'
                ) or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})
