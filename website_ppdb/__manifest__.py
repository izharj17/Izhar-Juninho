{
    'name': 'Website PPDB',
    'summary': 'PPDB Formulir Pendaftaran Front-End',
    'description': 'Module untuk menampilkan formulir PPDB pada website',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Website',
    'version': '1.0',
    'depends': ['website', 'base', 'mail'],
    'data': [
        'views/website_ppdb_templates_smp.xml',
        'views/website_ppdb_templates_sd.xml',
        'views/website_ppdb_templates_tk.xml',
        'views/website_ppdb_menu.xml',
        
    ],
    'installable': True,
    'application': True,
}
