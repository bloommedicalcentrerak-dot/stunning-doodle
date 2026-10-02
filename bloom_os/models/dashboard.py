from odoo import models, fields, api


class BloomDashboard(models.TransientModel):
    _name = 'bloom.dashboard'
    _description = 'Bloom Dashboard'

    total_patients = fields.Integer(
        string='Total Patients', compute='_compute_totals'
    )
    total_appointments = fields.Integer(
        string='Total Appointments', compute='_compute_totals'
    )
    total_laser_sessions = fields.Integer(
        string='Laser Sessions', compute='_compute_totals'
    )
    total_slimming_sessions = fields.Integer(
        string='Slimming Sessions', compute='_compute_totals'
    )

    @api.depends_context('uid')
    def _compute_totals(self):
        patient_count = self.env['bloom.patient'].search_count([])
        appointment_count = self.env['bloom.appointment'].search_count([])
        laser_count = self.env['bloom.laser'].search_count([])
        slimming_count = self.env['bloom.slimming'].search_count([])
        for rec in self:
            rec.total_patients = patient_count
            rec.total_appointments = appointment_count
            rec.total_laser_sessions = laser_count
            rec.total_slimming_sessions = slimming_count

    @api.model
    def action_open_dashboard(self):
        dashboard = self.create({})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dashboard',
            'res_model': 'bloom.dashboard',
            'view_mode': 'form',
            'res_id': dashboard.id,
            'target': 'current',
        }
