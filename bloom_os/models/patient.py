import re

from odoo import models, fields, api

EMIRATES_ID_RE = re.compile(r'(\d{3}-?\d{4}-?\d{7}-?\d)')


class BloomPatient(models.Model):
    _name = 'bloom.patient'
    _description = 'Bloom Patient'
    _order = 'name'

    name = fields.Char(string='Patient Name', required=True)
    phone = fields.Char(string='Phone')
    emirates_id = fields.Char(string='Emirates ID')
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
