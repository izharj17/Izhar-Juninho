from odoo import models, fields

class MasterSurah(models.Model):
    _name = "master.surah"
    _description = "Master Surah"
    _rec_name = "surah"

    surah = fields.Char('Nama Surah (سورة)')
    ayat = fields.Char('Jumlah Ayat (آية)')
    juz_ids = fields.Many2many('master.juz', 'Juz')