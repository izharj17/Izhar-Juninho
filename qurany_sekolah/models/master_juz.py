from odoo import models, fields

class MasterJuz(models.Model):
    _name = "master.juz"
    _description = "Master Juz"
    _rec_name = "juz"

    juz = fields.Char('Juz')
    code = fields.Char('Code')