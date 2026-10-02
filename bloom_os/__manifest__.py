{
    'name': 'Bloom OS Custom',
    'version': '1.1.0',
    'summary': 'Clinic Management System for Bloom Medical Center',
    'description': (
        'Patients, appointments, laser and slimming sessions, treatment '
        'packages, services, staff, rooms, payments and a clinic dashboard.'
    ),
    'author': 'Nehad',
    'website': 'https://github.com/bloommedicalcentrerak-dot/Bloom-OS',
    'category': 'Services',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/bloom_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/bloom_clinic_data.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/laser_view.xml',
        'views/slimming_view.xml',
        'views/package_view.xml',
        'views/payment_view.xml',
        'views/doctor_view.xml',
        'views/room_view.xml',
        'views/service_view.xml',
        'views/dashboard_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
