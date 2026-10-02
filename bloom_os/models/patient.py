import re

from odoo import models, fields, api

EMIRATES_ID_RE = re.compile(r'(\d{3}-?\d{4}-?\d{7}-?\d)')


class BloomPatient(models.Model):
    _name = 'bloom.patient'
    _description = 'Bloom Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    code = fields.Char(
        string='Patient Code', required=True, copy=False, readonly=True,
        default='New',
    )
    name = fields.Char(string='Patient Name', required=True, tracking=True)
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        string='Gender',
    )
    birthdate = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    street = fields.Char(string='Address')
    city = fields.Char(string='City')
    nationality = fields.Char(string='Nationality')
    emirates_id = fields.Char(string='Emirates ID')
    medical_history = fields.Text(string='Medical History')
    allergies = fields.Text(string='Allergies')
    emergency_contact_name = fields.Char(string='Emergency Contact')
    emergency_contact_phone = fields.Char(string='Emergency Phone')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    id_scan_raw = fields.Char(
        string='Scan ID',
        help=(
            'Focus this field and swipe/insert the card in the connected '
            'HID ID reader. The reader types the card data here like a '
            'keyboard; leaving the field automatically fills in the '
            'Patient Name and Emirates ID below.'
        ),
    )

    appointment_ids = fields.One2many(
        'bloom.appointment', 'patient_id', string='Appointments'
    )
    laser_ids = fields.One2many(
        'bloom.laser', 'patient_id', string='Laser Sessions'
    )
    slimming_ids = fields.One2many(
        'bloom.slimming', 'patient_id', string='Slimming Sessions'
    )
    package_ids = fields.One2many(
        'bloom.package', 'patient_id', string='Packages'
    )
    payment_ids = fields.One2many(
        'bloom.payment', 'patient_id', string='Payments'
    )

    @api.depends('birthdate')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.birthdate:
                born = rec.birthdate
                rec.age = today.year - born.year - (
                    (today.month, today.day) < (born.month, born.day)
                )
            else:
                rec.age = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals['code'] == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'bloom.patient'
                ) or 'New'
        return super().create(vals_list)

    @api.onchange('id_scan_raw')
    def _onchange_id_scan_raw(self):
        """Parse the raw text typed by a keyboard-emulation HID ID reader.

        HID readers behave like a keyboard: they type the card data into
        whichever field has focus, then send Enter/Tab. This splits the
        scanned text on common wedge-reader delimiters (tab, pipe, comma)
        and extracts an Emirates ID number and a name from it, so the user
        only needs to click into the "Scan ID" field and present the card.
        """
        raw = (self.id_scan_raw or '').strip()
        if not raw:
            return

        match = EMIRATES_ID_RE.search(raw)
        if match:
            self.emirates_id = match.group(1)
            raw = raw.replace(match.group(1), '')

        parts = [
            part.strip()
            for part in re.split(r'[\t|,;]+', raw)
            if part.strip()
        ]
        name_part = next(
            (part for part in parts if re.search(r'[A-Za-z]{2,}', part)),
            None,
        )
        if name_part and not self.name:
            self.name = name_part

        self.id_scan_raw = False
