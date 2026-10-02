from odoo import models, fields


class BloomDoctor(models.Model):
    _name = 'bloom.doctor'
    _description = 'Bloom Doctor'
    _order = 'name'

    name = fields.Char(string='Doctor Name', required=True)
    role = fields.Selection(
        [
            ('doctor', 'Doctor'),
            ('technician', 'Technician'),
            ('reception', 'Reception'),
            ('marketing', 'Marketing'),
        ],
        string='Role', default='doctor', required=True,
    )
    specialty = fields.Char(string='Specialty')
    department_id = fields.Many2one('bloom.department', string='Department')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(string='Active', default=True)

    evaluation_ids = fields.One2many(
        'bloom.staff_evaluation', 'staff_id', string='Evaluations'
    )
    attendance_ids = fields.One2many(
        'bloom.staff_attendance', 'staff_id', string='Attendance'
    )
