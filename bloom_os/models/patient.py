from odoo import models, fields


class BloomPatient(models.Model):
    _name = 'bloom.patient'
    _description = 'Bloom Patient'
    _order = 'name'

    name = fields.Char(string='Patient Name', required=True)
    phone = fields.Char(string='Phone')
    emirates_id = fields.Char(string='Emirates ID')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)

    appointment_ids = fields.One2many(
        'bloom.appointment', 'patient_id', string='Appointments'
    )
    laser_ids = fields.One2many(
        'bloom.laser', 'patient_id', string='Laser Sessions'
    )
    slimming_ids = fields.One2many(
        'bloom.slimming', 'patient_id', string='Slimming Sessions'
    )

    def action_view_chronicle(self):
        """Action to view patient's chronicle and tips."""
        self.ensure_one()
        chronicle_env = self.env['bloom.chronicle']
        chronicle = chronicle_env.analyze_patient(self.id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'bloom.chronicle',
            'res_id': chronicle.id,
            'view_mode': 'form',
            'target': 'current',
        }
