from odoo import models, fields, api


class BloomPayment(models.Model):
    _name = 'bloom.payment'
    _description = 'Bloom Payment'
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Reference', required=True, copy=False, readonly=True,
        default='New',
    )
    patient_id = fields.Many2one(
        'bloom.patient', string='Patient', required=True, ondelete='cascade'
    )
    date = fields.Date(
        string='Payment Date', required=True,
        default=fields.Date.context_today,
    )
    amount = fields.Float(string='Amount', required=True)
    payment_method = fields.Selection(
        [
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('transfer', 'Bank Transfer'),
        ],
        string='Payment Method',
        required=True,
        default='cash',
    )
    service_id = fields.Many2one('bloom.service', string='Service')
    appointment_id = fields.Many2one(
        'bloom.appointment', string='Appointment', ondelete='set null'
    )
    package_id = fields.Many2one(
        'bloom.package', string='Package', ondelete='set null'
    )
    notes = fields.Text(string='Notes')

    @api.onchange('service_id')
    def _onchange_service_id(self):
        if self.service_id and not self.amount:
            self.amount = self.service_id.price

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'bloom.payment'
                ) or 'New'
        return super().create(vals_list)
