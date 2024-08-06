{
    'name': 'Raport Siswa',
    'version': '14.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage Raport Students',
    'complexity': "easy",
    'author': 'AFajar',
    'website': '',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'report/arrasyid/print_raport_siswa_iep.xml',
        'report/arrasyid/print_raport_siswa_sts.xml',
        'report/arrasyid/print_raport_siswa_sas.xml',
        'report/arrasyid/print_raport_siswa_sat.xml',
        'views/raport_siswa_sts.xml',
        'views/raport_kampung_sawah.xml',
        'views/student_inherit_raport_view.xml',
        'views/raport_kampung_sawah_perilaku.xml',
        'data/ir_sequence_data.xml'
        
    ],
    'demo': [],
    'css': [],
    'qweb': [],
    'images': [
        'static/src/img/header.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
