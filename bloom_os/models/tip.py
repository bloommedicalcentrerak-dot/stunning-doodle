from odoo import models, fields


class BloomTip(models.Model):
    _name = 'bloom.tip'
    _description = 'Bloom Tip/Recommendation'

    title = fields.Char(string='Tip Title', required=True)
    description = fields.Text(string='Description', required=True)
    category = fields.Selection(
        [
            ('frequency', 'Session Frequency'),
            ('consistency', 'Consistency'),
            ('progress', 'Progress'),
            ('variety', 'Treatment Variety'),
            ('maintenance', 'Maintenance'),
            ('goals', 'Goals'),
        ],
        string='Category',
        required=True,
    )
    priority = fields.Selection(
        [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        string='Priority',
        default='medium',
    )
