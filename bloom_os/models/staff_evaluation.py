from odoo import models, fields


RATING_SELECTION = [
    ('1', '1 - Poor'),
    ('2', '2 - Below Average'),
    ('3', '3 - Average'),
    ('4', '4 - Good'),
    ('5', '5 - Excellent'),
]


class BloomStaffEvaluation(models.Model):
    _name = 'bloom.staff_evaluation'
    _description = 'Bloom Staff Evaluation'
    _order = 'evaluation_date desc'

    staff_id = fields.Many2one(
        'bloom.doctor', string='Doctor / Technician', required=True, ondelete='cascade'
    )
    evaluation_date = fields.Date(string='Evaluation Date', required=True)
    cross_selling = fields.Selection(RATING_SELECTION, string='Cross-selling')
    referral = fields.Selection(RATING_SELECTION, string='Referral')
    google_reviews = fields.Integer(string='Google Reviews Generated')
    upselling = fields.Selection(RATING_SELECTION, string='Upselling')
    complaints = fields.Integer(string='Complaints')
    client_feedback = fields.Text(string='Client Feedback')
    consent_form_compliance = fields.Boolean(string='Consent Form Compliance')
    teamwork = fields.Selection(RATING_SELECTION, string='Teamwork')
    welcome_greeting = fields.Selection(RATING_SELECTION, string='Welcome / Greeting')
    marketing_involvement = fields.Selection(RATING_SELECTION, string='Marketing Involvement')
    follow_up_done = fields.Boolean(string='Follow-up Done')
    renewed_clients = fields.Integer(string='Renewed Clients')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')
