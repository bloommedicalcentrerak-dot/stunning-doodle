from odoo import models, fields, api


class BloomLaser(models.Model):
    _name = 'bloom.laser'
    _description = 'Bloom Laser Session'
    _order = 'session_date desc'

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
    package_id = fields.Many2one(
        'bloom.package', string='Package', ondelete='set null'
    )
    session_date = fields.Datetime(string='Session Date', required=True)
    area = fields.Char(string='Treatment Area', required=True)
    machine = fields.Char(string='Machine Used')
    price = fields.Float(string='Price')
    notes = fields.Text(string='Notes')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    @api.onchange('service_id')
    def _onchange_service_id(self):
        if self.service_id:
            self.price = self.service_id.price

    @api.onchange('package_id')
    def _onchange_package_id(self):
        if self.package_id and not self.patient_id:
            self.patient_id = self.package_id.patient_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bloom.laser'
                ) or 'New'
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})
