from odoo import models, fields


class MasterYayasan(models.Model):
    _name = "master.yayasan"
    _description = "Master Yayasan"

    name = fields.Char('Yayasan')
    code = fields.Char('Code')
