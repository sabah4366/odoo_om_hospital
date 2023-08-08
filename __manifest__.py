{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'sequence':-100,
    'category': 'Hospital',
    'author': 'Abrus',
    'summary': 'Hospital Management System',
    'description': """ Hospital Management System   """,
    'depends': ['mail','product','report_xlsx'],
    'application':True,
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'data/mail_template_data.xml',
        'wizard/cancel_appointment_view.xml',
        'wizard/appointment_report_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/operation_view.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',
        'report/report.xml',
        'report/patient_report_template.xml',
        'report/appointment_details.xml',




    ],
    'auto_install': False,
    'licence':'LGPL-3'
}