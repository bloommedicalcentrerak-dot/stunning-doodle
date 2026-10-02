import math
from odoo import models, fields, api


class BloomChronicle(models.Model):
    _name = 'bloom.chronicle'
    _description = 'Bloom Session Chronicle & Tips'
    _order = 'patient_id, last_analysis_date desc'
    _sql_constraints = [
        (
            'bloom_chronicle_patient_unique',
            'unique(patient_id)',
            'Each patient can only have one chronicle record.',
        )
    ]

    patient_id = fields.Many2one(
        'bloom.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )

    # Session Statistics
    total_laser_sessions = fields.Integer(
        string='Total Laser Sessions', compute='_compute_session_stats', store=True
    )
    total_slimming_sessions = fields.Integer(
        string='Total Slimming Sessions', compute='_compute_session_stats', store=True
    )
    last_session_date = fields.Datetime(
        string='Last Session Date', compute='_compute_session_stats', store=True
    )
    average_days_between_sessions = fields.Float(
        string='Average Days Between Sessions',
        compute='_compute_session_stats',
        store=True,
    )

    # Progress Metrics
    weight_change = fields.Float(
        string='Weight Change (kg)', compute='_compute_progress_metrics', store=True
    )
    consistency_score = fields.Float(
        string='Consistency Score (0-100)',
        compute='_compute_progress_metrics',
        store=True,
    )

    # Tips and Recommendations
    recommended_tip_ids = fields.Many2many(
        'bloom.tip', string='Recommended Tips', compute='_compute_tips', store=True
    )
    tips_text = fields.Text(
        string='Generated Tips', compute='_compute_tips_text', store=True
    )
    last_analysis_date = fields.Datetime(string='Last Analysis Date', readonly=True)

    @api.depends('patient_id.laser_ids', 'patient_id.slimming_ids')
    def _compute_session_stats(self):
        """Compute session statistics for each patient."""
        for record in self:
            if not record.patient_id:
                record.total_laser_sessions = 0
                record.total_slimming_sessions = 0
                record.last_session_date = None
                record.average_days_between_sessions = 0
                continue

            patient = record.patient_id

            # Count sessions
            laser_sessions = patient.laser_ids.sorted('session_date')
            slimming_sessions = patient.slimming_ids.sorted('session_date')

            record.total_laser_sessions = len(laser_sessions)
            record.total_slimming_sessions = len(slimming_sessions)

            # Find last session
            all_sessions = laser_sessions + slimming_sessions
            if all_sessions:
                record.last_session_date = max(
                    all_sessions, key=lambda s: s.session_date
                ).session_date
            else:
                record.last_session_date = None

            # Calculate average days between sessions
            if len(all_sessions) > 1:
                dates = sorted([s.session_date for s in all_sessions])
                gaps = [
                    (dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)
                ]
                record.average_days_between_sessions = (
                    sum(gaps) / len(gaps) if gaps else 0
                )
            else:
                record.average_days_between_sessions = 0

    @api.depends('patient_id.laser_ids', 'patient_id.slimming_ids')
    def _compute_progress_metrics(self):
        """Compute progress metrics like weight change and consistency."""
        for record in self:
            if not record.patient_id:
                record.weight_change = 0
                record.consistency_score = 0
                continue

            patient = record.patient_id
            slimming_sessions = patient.slimming_ids.sorted('session_date')

            # Calculate weight change
            if len(slimming_sessions) >= 2:
                first_weight = slimming_sessions[0].weight
                last_weight = slimming_sessions[-1].weight
                if first_weight is not None and last_weight is not None:
                    record.weight_change = last_weight - first_weight
                else:
                    record.weight_change = 0
            else:
                record.weight_change = 0

            # Calculate consistency score (0-100)
            # Based on regularity of sessions
            all_sessions = (
                patient.laser_ids.sorted('session_date')
                + patient.slimming_ids.sorted('session_date')
            )
            if len(all_sessions) > 1:
                dates = sorted([s.session_date for s in all_sessions])
                gaps = [
                    (dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)
                ]

                # Calculate standard deviation of gaps
                if gaps:
                    avg_gap = sum(gaps) / len(gaps)
                    variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps)
                    # Lower variance (more consistent) = higher score
                    # Score: 100 - (std_dev / avg_gap * 50), capped at 0-100
                    std_dev = math.sqrt(variance)
                    consistency = 100 - (
                        std_dev / (avg_gap + 1) * 50
                    )  # +1 to avoid div by 0
                    record.consistency_score = max(0, min(100, consistency))
                else:
                    record.consistency_score = 100
            else:
                record.consistency_score = 0

    @api.depends('patient_id.laser_ids', 'patient_id.slimming_ids')
    def _compute_tips(self):
        """Generate recommended tips based on usage patterns."""
        for record in self:
            record.recommended_tip_ids = self._generate_tips(record.patient_id)

    @api.depends('recommended_tip_ids')
    def _compute_tips_text(self):
        """Convert recommended tips to readable text."""
        for record in self:
            if record.recommended_tip_ids:
                tips_text = '\n\n'.join(
                    [
                        f"• [{tip.category.upper()}] {tip.title}\n  {tip.description}"
                        for tip in record.recommended_tip_ids
                    ]
                )
                record.tips_text = tips_text
            else:
                record.tips_text = 'No tips available at this time.'

    def _generate_tips(self, patient):  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        """
        Analyze patient usage patterns and generate personalized tips.
        Returns a recordset of recommended tips.
        """
        if not patient:
            return self.env['bloom.tip']

        tips_env = self.env['bloom.tip']
        recommended_tips = tips_env.browse()

        # Get all sessions
        all_sessions = (
            patient.laser_ids.sorted('session_date')
            + patient.slimming_ids.sorted('session_date')
        )

        if not all_sessions:
            # No sessions yet - suggest getting started
            start_tip = tips_env.search(
                [('title', 'ilike', 'Begin your treatment journey')]
            )
            if not start_tip:
                # Create default tip if not exists
                return tips_env
            return start_tip

        # Calculate metrics for this patient
        dates = sorted([s.session_date for s in all_sessions])
        gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]

        # Average days between sessions
        avg_days_between = sum(gaps) / len(gaps) if gaps else 0

        # Calculate consistency score
        if len(all_sessions) > 1 and gaps:
            avg_gap = sum(gaps) / len(gaps)
            variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps)
            std_dev = math.sqrt(variance)
            consistency = 100 - (std_dev / (avg_gap + 1) * 50)
            consistency_score = max(0, min(100, consistency))
        else:
            consistency_score = 100

        # Tip 1: Session Frequency
        if avg_days_between > 30:  # Sessions are spaced more than 30 days apart
            freq_tip = tips_env.search(
                [('category', '=', 'frequency'), ('priority', '=', 'high')]
            )
            if freq_tip:
                recommended_tips |= freq_tip[:1]

        # Tip 2: Consistency
        if consistency_score < 50:
            consistency_tip = tips_env.search(
                [('category', '=', 'consistency'), ('priority', '=', 'high')]
            )
            if consistency_tip:
                recommended_tips |= consistency_tip[:1]

        # Tip 3: Progress (for slimming sessions)
        slimming_sessions = patient.slimming_ids.sorted('session_date')
        if len(slimming_sessions) > 2:
            weight_progress_tip = tips_env.search([('category', '=', 'progress')])
            if weight_progress_tip:
                recommended_tips |= weight_progress_tip[:1]

        # Tip 4: Treatment Variety
        laser_areas = set()
        slimming_programs = set()
        for laser in patient.laser_ids:
            if laser.area:
                laser_areas.add(laser.area)
        for slimming in patient.slimming_ids:
            if slimming.program:
                slimming_programs.add(slimming.program)

        if len(laser_areas) <= 1 and len(slimming_programs) <= 1:
            variety_tip = tips_env.search([('category', '=', 'variety')])
            if variety_tip:
                recommended_tips |= variety_tip[:1]

        # Tip 5: Maintenance
        if all_sessions:
            last_session = max(all_sessions, key=lambda s: s.session_date)
            days_since_last = (
                fields.Datetime.now() - last_session.session_date
            ).days
            if days_since_last > 60:
                maintenance_tip = tips_env.search([('category', '=', 'maintenance')])
                if maintenance_tip:
                    recommended_tips |= maintenance_tip[:1]

        return recommended_tips

    @api.model
    def analyze_patient(self, patient_id):
        """
        Public method to trigger analysis for a specific patient.
        Returns the chronicle record with updated tips.
        """
        patient = self.env['bloom.patient'].browse(patient_id)
        if not patient.exists():
            return None

        # Get or create chronicle for patient
        chronicle = self.search([('patient_id', '=', patient_id)], limit=1)
        if not chronicle:
            chronicle = self.create({'patient_id': patient_id})

        # Update analysis date
        chronicle.write({'last_analysis_date': fields.Datetime.now()})

        return chronicle

    @api.model
    def get_patient_tips(self, patient_id):
        """
        Get all tips and recommendations for a patient.
        Returns analysis data suitable for display.
        """
        patient = self.env['bloom.patient'].browse(patient_id)
        if not patient.exists():
            return None

        # Trigger analysis
        chronicle = self.analyze_patient(patient_id)

        return {
            'patient_name': patient.name,
            'total_laser_sessions': chronicle.total_laser_sessions,
            'total_slimming_sessions': chronicle.total_slimming_sessions,
            'last_session_date': chronicle.last_session_date,
            'average_days_between_sessions': chronicle.average_days_between_sessions,
            'weight_change': chronicle.weight_change,
            'consistency_score': chronicle.consistency_score,
            'tips': [
                {
                    'title': tip.title,
                    'description': tip.description,
                    'category': tip.category,
                    'priority': tip.priority,
                }
                for tip in chronicle.recommended_tip_ids
            ],
            'tips_text': chronicle.tips_text,
        }
