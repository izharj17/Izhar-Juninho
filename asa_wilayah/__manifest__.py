# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Wilayah',
    'Author': 'Achmad T. Zaini, Ifoel Arbeis',
    'Company' : '',
    'version': '1.0',
    'category': 'Wilayah',
    'summary': 'Wilayah',
    'description': """
        This module contains all the common features of Caroserie Pre-Sales Management.
    """,
    'depends': [
        "base",
        ],
    'data': [
        'security/wilayah_security.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False
}
