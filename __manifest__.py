{
    'name': 'Bloom OS Custom',
    'version': '1.0',
    'summary': 'Clinic Management System for Bloom Medical Center',
    'description': 'Patients, Appointments, Laser, Slimming, Dashboard',
    'author': 'Nehad',
    'category': 'Clinic',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/laser_view.xml',
        'views/slimming_view.xml',
        'views/dashboard_view.xml',
    ],
    'installable': True,
    'application': True,
}
