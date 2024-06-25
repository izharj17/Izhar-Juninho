from odoo import fields, models
class semester(models.Model):
    _name = 'op.semester'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Master Data Semester'
    _rec_name = 'semester_id'

    semester_id = fields.Char('Semester')
    code = fields.Char('Kode')