from odoo import models, fields

class BloomPatient(models.Model):
    _name = 'bloom.patient'
    _description = 'Bloom Patient'

    name = fields.Char(string='Patient Name')
    phone = fields.Char(string='Phone')
    emirates_id = fields.Char(string='Emirates ID')
    notes = fields.Text(string='Notes')
