from odoo import models, fields, api


class BloomPackage(models.Model):
    _name = 'bloom.package'
    _description = 'Bloom Treatment Package'
    _order = 'start_date desc, id desc'

    name = fields.Char(
        string='Reference', required=True, copy=False, readonly=True,
        default='New',
    )
    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    service_id = fields.Many2one('bloom.service', string='Service')
    total_sessions = fields.Integer(string='Total Sessions', default=1)
    used_sessions = fields.Integer(
        string='Used Sessions', compute='_compute_sessions'
    )
    remaining_sessions = fields.Integer(
        string='Remaining Sessions', compute='_compute_sessions'
    )
    price = fields.Float(string='Package Price')
    start_date = fields.Date(
        string='Start Date', default=fields.Date.context_today
    )
    end_date = fields.Date(string='End Date')
    notes = fields.Text(string='Notes')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    laser_ids = fields.One2many(
        'bloom.laser', 'package_id', string='Laser Sessions'
    )
    slimming_ids = fields.One2many(
        'bloom.slimming', 'package_id', string='Slimming Sessions'
    )

    @api.depends(
        'total_sessions', 'laser_ids.state', 'slimming_ids.state'
    )
    def _compute_sessions(self):
        for rec in self:
            used = len(rec.laser_ids.filtered(lambda s: s.state == 'done'))
            used += len(
                rec.slimming_ids.filtered(lambda s: s.state == 'done')
            )
            rec.used_sessions = used
            rec.remaining_sessions = rec.total_sessions - used

    @api.onchange('service_id')
    def _onchange_service_id(self):
        if self.service_id and not self.price:
            self.price = self.service_id.price

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bloom.package'
                ) or 'New'
        return super().create(vals_list)

    def action_start(self):
        self.write({'state': 'running'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})
