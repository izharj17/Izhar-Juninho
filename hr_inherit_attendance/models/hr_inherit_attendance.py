from odoo import fields, models, api

class hr_inherit_attendance(models.Model):
    _inherit = "hr.attendance"

    status_kehadiran = fields.Selection([
        ('ot', 'Tepat Waktu'),
        ('tlb', 'Terlambat'),
    ], string='Status')
    long_position = fields.Char('Long Position')
    lat_position = fields.Char('Lat Position')
