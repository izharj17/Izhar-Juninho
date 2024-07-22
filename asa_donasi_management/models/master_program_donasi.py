from odoo import models, fields

class master_program_donasi(models.Model):
    _name = "master.program.donasi"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Donasi"
    _rec_name = 'nama_program_donasi'

    nama_program_donasi = fields.Char('Nama Program Donasi')
    kode = fields.Char('Kode')