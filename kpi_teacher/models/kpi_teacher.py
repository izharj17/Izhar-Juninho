from odoo import models, fields, api

class KpiTeacher(models.Model):
    _name = 'kpi.teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Management"
    _rec_name = 'guru_id'

    guru_id = fields.Many2one('hr.employee', 'Guru')
    department_id = fields.Many2one('hr.department', 'Bagian', related='guru_id.department_id')
    template_question_id = fields.Many2one('master.question', 'Jenis KPI ', required=True)
    kpi_ids = fields.One2many('kpi.teacher.line', 'kpi_teacher_id', string='KPI Line')
    tanggal_kpi = fields.Date('Tanggal', required=True, default=lambda self: fields.Date.today(),
        tracking=True)
    nilai_total_kpi = fields.Integer('Nilai Total')
    nama_sekolah = fields.Many2one('res.company', 'Sekolah')

    @api.onchange('template_question_id')
    def _onchange_template_question_id(self):
        if self.template_question_id:
            # Hapus baris KPI yang ada
            self.kpi_ids.unlink()

            # Ambil pertanyaan dari MasterQuestion dan buat baris KPI
            for question_line in self.template_question_id.master_question_ids:
                kpi_line_vals = {
                    'kpi_teacher_id': self.id,
                    'question': question_line.question,
                    'ketuntasan': '',  # Anda dapat menetapkan nilai default untuk 'jawaban' jika diperlukan
                    'file_kpi': '',
                }
                self.kpi_ids.create(kpi_line_vals)


class KpiTeacherLine(models.Model):
    _name = 'kpi.teacher.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line"

    kpi_teacher_id = fields.Many2one('kpi.teacher', string='Survey')
    question = fields.Text('Nama Kegiatan', size=2)
    ketuntasan = fields.Boolean('Ketuntasan', default=True, tracking=True, size=4)
    file_kpi = fields.Binary('Unggah Dokumen', file_kpi=True, size=4)