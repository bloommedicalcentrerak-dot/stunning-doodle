from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BloomPurchase(models.Model):
    _name = 'bloom.purchase'
    _description = 'Bloom Purchase Record'
    _order = 'order_date desc, id desc'

    name = fields.Char(string='Item Name', required=True)
    department_id = fields.Many2one(
        'bloom.department', string='Department', required=True, ondelete='restrict'
    )
    supplier = fields.Char(string='Supplier', required=True)
    quantity_ordered = fields.Float(string='Ordered Quantity', required=True, default=1.0)
    quantity_received = fields.Float(string='Received Quantity', default=0.0)
    unit_price = fields.Float(string='Unit Price')
    total_price = fields.Float(
        string='Total Price', compute='_compute_total_price', store=True
    )
    order_date = fields.Date(
        string='Order Date', required=True, default=fields.Date.context_today
    )
    expected_delivery_date = fields.Date(string='Expected Delivery Date')
    received_date = fields.Date(string='Received Date')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('ordered', 'Ordered'),
            ('partial', 'Partially Received'),
            ('received', 'Received'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        required=True,
        default='draft',
    )
    remaining_quantity = fields.Float(
        string='Remaining Quantity', compute='_compute_remaining_quantity', store=True
    )
    is_overdue = fields.Boolean(string='Overdue', compute='_compute_alerts', store=True)
    is_low_stock = fields.Boolean(
        string='Low Stock', compute='_compute_alerts', store=True
    )
    alert_message = fields.Char(string='Alert', compute='_compute_alerts', store=True)
    current_stock = fields.Float(string='Current Stock')
    minimum_stock = fields.Float(string='Minimum Stock')
    notes = fields.Text(string='Notes')
    invoice_file = fields.Binary(string='Invoice')
    invoice_filename = fields.Char(string='Invoice Filename')
    quotation_file = fields.Binary(string='Quotation')
    quotation_filename = fields.Char(string='Quotation Filename')
    receipt_file = fields.Binary(string='Delivery Receipt')
    receipt_filename = fields.Char(string='Delivery Receipt Filename')
    other_document = fields.Binary(string='Other Document')
    other_document_filename = fields.Char(string='Other Document Filename')

    @api.depends('quantity_ordered', 'unit_price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.quantity_ordered * rec.unit_price

    @api.depends('quantity_ordered', 'quantity_received')
    def _compute_remaining_quantity(self):
        for rec in self:
            rec.remaining_quantity = max(rec.quantity_ordered - rec.quantity_received, 0.0)

    @api.depends(
        'expected_delivery_date',
        'state',
        'current_stock',
        'minimum_stock',
        'quantity_ordered',
        'quantity_received',
    )
    def _compute_alerts(self):
        today = fields.Date.context_today(self)
        for rec in self:
            alerts = []
            rec.is_overdue = bool(
                rec.expected_delivery_date
                and rec.expected_delivery_date < today
                and rec.state not in ('received', 'cancelled')
            )
            rec.is_low_stock = bool(
                rec.minimum_stock and rec.current_stock <= rec.minimum_stock
            )
            if rec.is_overdue:
                alerts.append('Delivery overdue')
            if rec.state == 'partial':
                alerts.append('Partially received')
            if rec.is_low_stock:
                alerts.append('Stock is near minimum')
            rec.alert_message = ', '.join(alerts)

    @api.constrains('quantity_ordered', 'quantity_received', 'current_stock', 'minimum_stock')
    def _check_quantities(self):
        for rec in self:
            if rec.quantity_ordered < 0 or rec.quantity_received < 0:
                raise ValidationError(_('Quantities cannot be negative.'))
            if rec.quantity_received > rec.quantity_ordered:
                raise ValidationError(
                    _('Received quantity cannot be greater than ordered quantity.')
                )
            if rec.current_stock < 0 or rec.minimum_stock < 0:
                raise ValidationError(_('Stock values cannot be negative.'))

    def action_set_ordered(self):
        self.write({'state': 'ordered'})

    def action_set_partial(self):
        self.write({'state': 'partial'})

    def action_set_received(self):
        for rec in self:
            rec.write(
                {
                    'state': 'received',
                    'received_date': rec.received_date or fields.Date.context_today(rec),
                    'quantity_received': rec.quantity_ordered,
                }
            )

    def action_set_cancelled(self):
        self.write({'state': 'cancelled'})

    def action_set_draft(self):
        self.write({'state': 'draft'})
