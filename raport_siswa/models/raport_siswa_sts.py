from odoo import models, fields, api


class RaportSiswaSTS(models.Model):
    _name = "raport.siswa.sts"
    _description = "Raport Siswa STS"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'jenis_raport'

    kode_seq = fields.Char(string="Raport ID", readonly=True)
    jenis_raport = fields.Selection([
        ('STS', 'STS'),
        ('SAS', 'SAS'),
        ('SAT', 'SAT'),
    ], 'Jenis Raport')
    student_id = fields.Many2one('op.student', 'Student', tracking=True)
    nis_nisn = fields.Char('NIS/NISN', related='student_id.nis')
    sekolah_id = fields.Many2one('res.company', 'Sekolah', default=lambda self: self.env['res.company'].search([('name', '=', 'SD Islam Arrasyid')], limit=1).id)
    alamat_sekolah = fields.Char('Alamat Sekolah', related='sekolah_id.street')
    kelas_id = fields.Many2one('op.course', 'Kelas', readonly=False)
    grade_id = fields.Many2one('op.batch', 'Rombel')
    semester_id = fields.Selection([
        ('1', '1 (Ganjil)'),
        ('2', '2 (Genap)'),
    ], 'Semester')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Pelajaran')
    # jenis_raport = fields.Selection([
    #     ('1', 'STS'),
    #     ('2', 'SAT'),
    #     ('3', 'SAT'),
    # ], 'Raport')
    raport_siswa_ids = fields.One2many('raport.siswa.line', 'raport_id', 'Raport Line')
    mulok_siswa_ids = fields.One2many('op.student.mulok', 'raport_id', 'Mulok')
    karakter_siswa_ids = fields.One2many('op.student.karakter', 'raport_id', 'Karakter')
    # kegiatan_siswa_ids = fields.One2many('op.activity', 'raport_id', 'Kegiatan')
    perkembangan_siswa_ids = fields.One2many('op.student.priodik', 'raport_id', 'Priodik')
    prestasi_siswa_ids = fields.One2many('op.student.prestasi', 'raport_id', 'Prestasi')
    ksmpln_saran = fields.Text('Kesimpulan Saran')
    keputusan_siswa = fields.Text('Keputusan')
    ttd_ortu = fields.Text('Orang Tua / Wali')
    ttd_walas = fields.Text('Wali Kelas')
    ttd_kepsek = fields.Text('Kepala Sekolah')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('publish', 'Publish'),
        ('cancel', 'Cancel'),
    ], string='State', readonly=True, default='draft', required=True, tracking=True)

    @api.depends('student_id.course_detail_ids')
    def _compute_kelas_id(self):
        for record in self:
            # Ambil kelas dari course_detail_ids pertama (jika ada)
            course_detail = record.student_id.course_detail_ids and record.student_id.course_detail_ids[0]
            if course_detail:
                record.kelas_id = course_detail.course_id

    # # Menambahkan fungsi on_change untuk mengupdate kelas_id saat course_detail_ids berubah
    # @api.onchange('student_course_ids')
    # def _onchange_student_course_ids(self):
    #     # Mengambil kelas dari course_detail_ids pertama (jika ada)
    #     course_detail = self.student_id.course_detail_ids and self.student_id.course_detail_ids[0]
    #     if course_detail:
    #         self.kelas_id = course_detail.course_id

    @api.onchange('student_id')
    def _onchange_student_id(self):
        # Cek apakah ada student yang dipilih
        if self.student_id:
            # Ambil kelas dari course_detail_ids pertama (jika ada)
            course_detail = self.student_id.course_detail_ids and self.student_id.course_detail_ids[0]
            if course_detail:
                self.kelas_id = course_detail.course_id
                
    @api.onchange('student_id')
    def onchange_student_id_grade(self):
        if self.student_id:
            self.grade_id = self.student_id.rombel.id

    def func_approve(self):
        if self.state == 'draft':
            self.state = 'approve'

    def func_publish(self):
        if self.state == 'approve':
            self.state = 'publish'

    def func_cancel(self):
        if self.state == 'approve':
            self.state = 'cancel'

    def func_set_draft(self):
        if self.state == 'cancel':
            self.state = 'draft'

    # @api.model
    # def create(self, vals):
    #     vals['kode_seq'] = self.env['ir.sequence'].next_by_code('raport.siswa.sts') or 'RAP/STS/'
    #     msg_body = 'Raport created'
    #     for msg in self:
    #         msg.message_post(body=msg_body)
    #     result = super(RaportSiswaSTS, self).create(vals)
    #     return result

class RaportSiswaline(models.Model):
    _name = "raport.siswa.line"
    _description = "Raport Siswa Line"

    raport_id = fields.Many2one('raport.siswa.sts')
    subject_id = fields.Many2one('op.subject', 'Mata Pelajaran')
    nilai_akhir = fields.Integer('Nilai Akhir', size=8)
    note = fields.Text('Capaian Kompetensi', size=8)
    note2 = fields.Text('Catatan Kompetensi', size=8)

class OpStudentRaport(models.Model):
    _inherit = "op.student"

    raport_sts_count = fields.Integer(compute='compute_count_raport_sts')

    def get_raport_sts(self):
        action = self.env.ref('openeducat_core.'
                              'raport_siswa_sts_action').read()[0]
        action['domain'] = [('student_id', 'in', self.ids)]
        return action

    def compute_count_raport_sts(self):
        for record in self:
            record.raport_sts_count = self.env['raport.siswa.sts'].search_count(
                [('student_id', '=', self.id)])