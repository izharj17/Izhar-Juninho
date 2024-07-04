from odoo import models, fields, api

class MasterQuestion(models.Model):
    _name = 'master.question'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Question"

    name = fields.Char('Template')
    master_question_ids = fields.One2many('master.question.line', 'master_question_id', 'Master Question Line')

class MasterQuestionLine(models.Model):
    _name = 'master.question.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Question Line"

    master_question_id = fields.Many2one('master.question', 'Master Question ID')
    question = fields.Text('Nama Kegiatan')
    bobot_pekan = fields.Integer('Bobot')


