from odoo import models, fields, api
import math

class KpiTeacher(models.Model):
    _name = 'kpi.teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Management"
    _rec_name = 'guru_id'

    #Identitas
    guru_id = fields.Many2one('hr.employee', 'Guru')
    department_id = fields.Many2one('hr.department', 'Bagian', related='guru_id.department_id')
    
    #Jenis KPI
    template_question_id = fields.Many2one('master.question', 'Jenis KPI', required=True)
    
    #Isi Tugas KPI
    kpi_ids = fields.One2many('kpi.teacher.line', 'kpi_teacher_id', string='KPI Line')
    
    #Validitas KPI
    pekan_kpi = fields.Selection([
        ('1', 'Pekan 1'),
        ('2', 'Pekan 2'),
        ('3', 'Pekan 3'),
        ('4', 'Pekan 4'),
    ], 'Pekan')
    nilai_total_pekanan = fields.Float('Nilai Total Pekanan (Max 25)', compute='_compute_nilai_total_pekanan', store=True, readonly=True)
    nilai_total_bulanan = fields.Float('Nilai Total Bulanan (Max 100)')
    bulan_kpi = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
    ], 'Bulan')
    
    #Status KPI
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved')
    ], string='State', readonly=True, default='draft', required=True, tracking=True)
    
    def func_approve(self):
        if self.state == 'draft':
            self.state = 'approve'

    def func_back_to_draft(self):
        if self.state == 'approve':
            self.state = 'draft'

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
            total_score = sum(line.bobot for line in record.kpi_ids if line.ketuntasan)
            record.nilai_total_pekanan = min(total_score, 25)  # Cap the score at 25

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

