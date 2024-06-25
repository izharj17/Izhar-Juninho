from odoo import fields, models
class fakultas(models.Model):
    _name = 'op.fakultas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Master Data Fakultas'
    _rec_name = 'fakultas_id'

    fakultas_id = fields.Char('Nama Fakultas')
    code_fakultas = fields.Char('Kode Fakultas')