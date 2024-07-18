from odoo import models, fields, api

class master_tipe_penerima(models.Model):
    _name = "master.tipe.penerima"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Tipe Penerima"
    _rec_name = 'nama_tipe_penerima'

    nama_tipe_penerima = fields.Char('Nama penerima')
    code = fields.Char('Kode')