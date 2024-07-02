from odoo import models, fields, api
import math

class KpiTeacher(models.Model):
    _name = 'kpi.teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Management"
    _rec_name = 'guru_id'

    guru_id = fields.Many2one('hr.employee', 'Guru')
    department_id = fields.Many2one('hr.department', 'Bagian', related='guru_id.department_id')
    template_question_id = fields.Many2one('master.question', 'Jenis KPI ', required=True)
    kpi_ids = fields.One2many('kpi.teacher.line', 'kpi_teacher_id', string='KPI Line')
    tanggal_kpi = fields.Date('Tanggal', required=True, default=lambda self: fields.Date.today(), tracking=True)
    nilai_total_pekanan = fields.Float('Nilai Total Pekanan (Max 25)', compute='_compute_nilai_total_pekanan', store=True, readonly=True)
    nilai_total_bulanan = fields.Float('Nilai Total Bulanan (Max 100')
    nama_sekolah = fields.Many2one('res.company', 'Sekolah', default=lambda self: self.env['res.company'].search([('name', '=', 'Sekolah Alam Tangerang')], limit=1))

    @api.onchange('template_question_id')
    def _onchange_template_question_id(self):
        if self.template_question_id:
            self.kpi_ids.unlink()
            for question_line in self.template_question_id.master_question_ids:
                kpi_line_vals = {
                    'kpi_teacher_id': self.id,
                    'question': question_line.question,
                    'bobot': question_line.bobot_pekan,
                    'ketuntasan': False,
                    'file_kpi': '',
                }
                self.kpi_ids.create(kpi_line_vals)

    @api.depends('kpi_ids.ketuntasan')
    def _compute_nilai_total_pekanan(self):
        for record in self:
            number_of_questions = len(record.kpi_ids)
            if number_of_questions > 0:
                point_per_question = 100 / number_of_questions
                completed_questions = sum(1 for line in record.kpi_ids if line.ketuntasan)
                total_score = point_per_question * completed_questions
                record.nilai_total_pekanan = min(total_score, 100)  # Cap the score at 100
            else:
                record.nilai_total_pekanan = 0

class KpiTeacherLine(models.Model):
    _name = 'kpi.teacher.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line"

    kpi_teacher_id = fields.Many2one('kpi.teacher', string='Survey')
    question = fields.Text('Nama Kegiatan')
    bobot = fields.Integer('Bobot')
    ketuntasan = fields.Boolean('Ketuntasan', default=False, tracking=True)
    file_kpi = fields.Binary('Unggah Dokumen')

    @api.onchange('ketuntasan')
    def _onchange_ketuntasan(self):
        if self.kpi_teacher_id:
            self.kpi_teacher_id._compute_nilai_total_pekanan()
