from odoo import models, fields

class BloomDashboard(models.Model):
    _name = 'bloom.dashboard'
    _description = 'Bloom Dashboard'

    total_patients = fields.Integer(string='Total Patients')
    total_appointments = fields.Integer(string='Total Appointments')
    total_laser_sessions = fields.Integer(string='Laser Sessions')
    total_slimming_sessions = fields.Integer(string='Slimming Sessions')
