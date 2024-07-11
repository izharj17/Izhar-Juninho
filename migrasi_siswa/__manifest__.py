{
    'name': 'Migrasi Siswa',
    'version': '14.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage and Record Student Migration',
    'complexity': "easy",
    'author': 'AFajar',
    'website': '',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/migration_view.xml'
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
