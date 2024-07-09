# -*- coding: utf-8 -*-
{
    "name": "BSI Payment Integration",
    "version": "1.01",
    "author": "Ifoel Arbeis",
    'images': ['static/description/icon.png'],
    "license": "",
    "category": "Custom",
    "summary": "Integration Create and Payment Invoice",
    "website": "",
    "depends": ["account","openeducat_core"],
    "data": [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/email_template_view.xml',
        'views/bsi_config_view.xml',
        'views/account_move_view.xml',
        'views/deposit_bsi_view.xml',
        'wizard/mass_create_invoice_bsi_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
