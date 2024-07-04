{
    'name': 'KPI Teacher',
    'version': '14.0.1.0',
    'license': 'LGPL-3',
    'category': 'User',
    "sequence": 1,
    'summary': 'User',
    'complexity': "easy",
    'author': 'AFajarR',
    'website': '',
    'depends': ['base', 'hr'],
    'data': [
            'security/ir.model.access.csv',
            'views/kpi_teacher_views.xml',
            'views/master_question_views.xml',
            'views/kpi_supervisi_views.xml',
            ],
    'demo': [

            ],
    'css': [

        ],
    'qweb': [

            ],
    'images': [

            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}