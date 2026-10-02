from datetime import datetime, time

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
    today_appointments = fields.Integer(
        string="Today's Appointments", compute='_compute_totals'
    )
    total_laser_sessions = fields.Integer(
        string='Laser Sessions', compute='_compute_totals'
    )
    total_slimming_sessions = fields.Integer(
        string='Slimming Sessions', compute='_compute_totals'
    )
    total_packages = fields.Integer(
        string='Treatment Packages', compute='_compute_totals'
    )
    total_payments = fields.Integer(
        string='Payments', compute='_compute_totals'
    )
    total_payment_amount = fields.Float(
        string='Collected Amount', compute='_compute_totals'
    )

    @api.depends_context('uid')
    def _compute_totals(self):
        today = fields.Date.context_today(self)
        day_start = datetime.combine(today, time.min)
        day_end = datetime.combine(today, time.max)
        patient_count = self.env['bloom.patient'].search_count([])
        appointment_count = self.env['bloom.appointment'].search_count([])
        today_count = self.env['bloom.appointment'].search_count([
            ('date', '>=', day_start),
            ('date', '<=', day_end),
        ])
        laser_count = self.env['bloom.laser'].search_count([])
        slimming_count = self.env['bloom.slimming'].search_count([])
        package_count = self.env['bloom.package'].search_count([])
        payments = self.env['bloom.payment'].search([])
        payment_amount = sum(payments.mapped('amount'))
        for rec in self:
            rec.total_patients = patient_count
            rec.total_appointments = appointment_count
            rec.today_appointments = today_count
            rec.total_laser_sessions = laser_count
            rec.total_slimming_sessions = slimming_count
            rec.total_packages = package_count
            rec.total_payments = len(payments)
            rec.total_payment_amount = payment_amount

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
