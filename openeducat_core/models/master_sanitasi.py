from odoo import models, fields


class MasterSanitasi(models.Model):
    _name = "master.sanitasi"
    _description = "Master Sanitasi"

    name = fields.Char('Variabel')
    code = fields.Char('Code')
