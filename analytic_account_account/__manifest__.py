# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Accounting with Analytic Account",
    "summary": "Introduces Analytic Account (AA) in invoices and "
    "Accounting Entries with clearing account",
    "version": "14.0.1.0.2",
    "author": "AFajar, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": ["account", 'sale', 'base_accounting_kit'],
    "license": "LGPL-3",
    "data": [
        "views/account_move_aa.xml",
        "views/aa_payment_views.xml",
        "views/so_inherit.xml",
        "views/cash_masuk_group_tag.xml",
    ],
    "installable": True,
}
