from odoo import models, fields, api


class rab_wakaf(models.Model):
    _name = "rab.wakaf"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "RAB Wakaf"

    wakaf_id = fields.Many2one('wakaf.management', string='Wakaf', required=True)
    category_wakaf_id = fields.Many2one('master.category.wakaf', 'Kategori Wakaf')
    tipe_wakaf_id = fields.Selection([
        ('wk', 'Wakaf Kolektif'),
        ('wa', 'Wakaf Abadi'),
        ('wb', 'Wakaf Berjangka'),
    ], string='Tipe Wakaf')

