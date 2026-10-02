# Chronicle Tips Feature Documentation

## Overview

The `/chronicle tips` feature analyzes a patient's session history and provides personalized recommendations based on their usage patterns. It helps patients understand their treatment consistency, progress, and provides actionable tips to optimize their treatment plans.

## Features

### 1. Session Analytics
- **Total Sessions Tracked**: Counts laser and slimming sessions for each patient
- **Session Frequency**: Analyzes the average days between sessions
- **Last Session Date**: Tracks the most recent treatment
- **Consistency Score**: Measures how regularly a patient schedules sessions (0-100)

### 2. Progress Metrics
- **Weight Change**: Tracks weight changes from slimming sessions
- **Treatment Variety**: Monitors diversity of treatment areas and programs
- **Session Patterns**: Identifies trends in patient behavior

### 3. Automated Tip Generation
The system generates personalized tips based on:
- **Frequency Optimization**: Recommends increasing session frequency if sessions are spaced >30 days apart
- **Consistency Improvement**: Suggests more regular scheduling if consistency score is low
- **Progress Celebration**: Acknowledges and encourages continued treatment progress
- **Treatment Variety**: Recommends exploring different treatment options
- **Maintenance Reminders**: Suggests booking sessions if >60 days have passed
- **Goal Setting**: Encourages patients to set clear treatment objectives

## Models

### bloom.tip
Stores predefined tip templates with categories and priorities.
- **Fields**:
  - `title`: Tip title
  - `description`: Detailed tip text
  - `category`: Frequency, consistency, progress, variety, maintenance, or goals
  - `priority`: High, medium, or low priority

### bloom.chronicle
Tracks session analytics and recommended tips for each patient.
- **Fields**:
  - `patient_id`: Related patient
  - `total_laser_sessions`: Count of laser sessions
  - `total_slimming_sessions`: Count of slimming sessions
  - `last_session_date`: Most recent session
  - `average_days_between_sessions`: Average gap between sessions
  - `weight_change`: Weight change from slimming sessions
  - `consistency_score`: Regularity score (0-100)
  - `recommended_tip_ids`: Many-to-many relationship with tips
  - `tips_text`: Human-readable tip recommendations
  - `last_analysis_date`: When analysis was last run

## Usage

### For Patients
1. Navigate to the patient record
2. Click the "Tips & Chronicle" tab
3. Click "View My Tips & Analysis" button
4. View personalized recommendations and session statistics

### For Administrators
1. Create new tip templates in "Tip Templates" menu
2. Customize tip content for different categories
3. Tips are automatically matched to patients based on their usage patterns

## Tip Categories

### Frequency (Session Scheduling)
- Encouraging regular appointments
- Optimal session spacing recommendations

### Consistency (Schedule Regularity)
- Measuring and improving session reliability
- Tracking patterns over time

### Progress (Treatment Outcomes)
- Celebrating achievements
- Encouraging continuation

### Variety (Treatment Options)
- Exploring different treatment areas
- Combining multiple modalities

### Maintenance (Long-term Care)
- Scheduling follow-up sessions
- Sustaining results

### Goals (Patient Objectives)
- Setting clear treatment targets
- Reviewing progress against goals

## Algorithm Details

### Consistency Score Calculation
The consistency score is calculated using standard deviation of session gaps:
- Score = 100 - (std_dev / avg_gap * 50)
- Capped between 0-100
- Higher score indicates more regular sessions

### Tip Selection Logic
1. **Frequency**: If avg_days_between > 30 days → recommend frequency optimization
2. **Consistency**: If consistency_score < 50 → recommend consistency improvement
3. **Progress**: If > 2 slimming sessions → acknowledge progress
4. **Variety**: If ≤ 1 laser area AND ≤ 1 slimming program → recommend variety
5. **Maintenance**: If > 60 days since last session → recommend maintenance

## Data Files

### Default Tips
12 default tips are included:
- 2 frequency tips
- 2 consistency tips
- 2 progress tips
- 2 variety tips
- 2 maintenance tips
- 2 goals tips

These are loaded when the module is installed and can be modified or supplemented by administrators.

## Integration Points

### Patient Form
- New "Tips & Chronicle" tab with quick access button
- One-click access to patient analysis

### Menu
- "Chronicle & Tips" menu item under Bloom OS
- "Tip Templates" menu for managing tips

### Database
- New models automatically included in security rules
- Computed fields auto-update when sessions are added

## Performance Considerations

- Computed fields are stored in database for quick access
- Analysis runs on-demand via `analyze_patient()` method
- Large session histories are handled efficiently with sorted queries

## API Methods

### analyze_patient(patient_id)
Triggers analysis for a specific patient and returns the chronicle record.
```python
chronicle = env['bloom.chronicle'].analyze_patient(patient_id)
```

### get_patient_tips(patient_id)
Returns formatted analysis data including all metrics and tips.
```python
tips_data = env['bloom.chronicle'].get_patient_tips(patient_id)
# Returns: {
#     'patient_name': str,
#     'total_laser_sessions': int,
#     'total_slimming_sessions': int,
#     'last_session_date': datetime,
#     'average_days_between_sessions': float,
#     'weight_change': float,
#     'consistency_score': float,
#     'tips': [{'title': str, 'description': str, ...}],
#     'tips_text': str
# }
```

## Future Enhancements

- Email notifications with personalized tips
- SMS reminders for scheduled maintenance
- Mobile app integration
- Export reports with tips and progress
- AI-powered tip personalization based on patient outcomes
- Integration with appointment booking system
