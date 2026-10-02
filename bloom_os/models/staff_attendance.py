from odoo import models, fields, api


STATUS_SELECTION = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('leave', 'Leave'),
]


class BloomStaffAttendance(models.Model):
    _name = 'bloom.staff_attendance'
    _description = 'Bloom Staff Attendance'
    _order = 'date desc'

    staff_id = fields.Many2one(
        'bloom.doctor', string='Staff Member', required=True, ondelete='cascade'
    )
    date = fields.Date(string='Date', required=True)
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    status = fields.Selection(
        STATUS_SELECTION, string='Status', default='present', required=True
    )
    overtime_hours = fields.Float(string='Overtime Hours', compute='_compute_overtime_hours', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('check_in', 'check_out')
    def _compute_overtime_hours(self):
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                worked = attendance.check_out - attendance.check_in
                worked_hours = worked.total_seconds() / 3600.0
                attendance.overtime_hours = max(worked_hours - 8.0, 0.0)
            else:
                attendance.overtime_hours = 0.0
