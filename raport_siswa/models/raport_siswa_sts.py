import time
import datetime
from odoo import models, fields, api

class RaportSiswaSTS(models.Model):
    _name = "raport.siswa.sts"
    _description = "Raport Siswa STS"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit mail.thread and mail.activity.mixin here
    _rec_name = 'jenis_raport'

    kode_seq = fields.Char(string="Raport ID", readonly=True)
    jenis_raport = fields.Selection([
        ('STS', 'STS'),
        ('SAS', 'SAS'),
        ('SAT', 'SAT'),
    ], 'Jenis Raport')

    # Identitas
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

    # Isi Raport
    raport_siswa_ids = fields.One2many('raport.siswa.line', 'raport_id', 'Raport Line')
    mulok_siswa_ids = fields.One2many('op.student.mulok', 'raport_id', 'Mulok')
    prestasi_siswa_ids = fields.One2many('op.student.prestasi', 'raport_id', 'Prestasi')
    kegiatan_siswa_ids = fields.One2many('raport.siswa.kegiatan', 'raport_id', 'Kegiatan')

    # Periodik
    tinggi_bdn = fields.Integer('Tinggi Badan')
    berat_bdn = fields.Integer('Berat Badan')
    lingkar_kpl = fields.Integer('Lingkar Kepala')
    pendengaran = fields.Selection([
        ('1', 'Normal'),
        ('2', 'Tidak Normal'),
    ], 'Pendengaran')
    penglihatan = fields.Selection([
        ('1', 'Normal'),
        ('2', 'Tidak Normal'),
    ], 'Penglihatan')
    gigi = fields.Selection([
        ('1', 'Berlubang'),
        ('2', 'Tidak Berlubang'),
    ], 'Gigi')

    # Ketidakhadiran
    sakit = fields.Integer(string="Sakit")
    ijin = fields.Integer(string="Ijin")
    tanpa_ket = fields.Integer(string="Tanpa Keterangan")
    
    #Karakter
    mandiri = fields.Text('Mandiri')
    disiplin = fields.Text('Disiplin')
    tertib = fields.Text('Tertib')
    percaya_diri = fields.Text('Percaya Diri')
    tanggung_jawab = fields.Text('Tanggung Jawab')
    kerjasama = fields.Text('Kerja Sama')
    kepemimpinan = fields.Text('Kepemimpinan')

    # Keputusan dan Saran
    ksmpln_saran = fields.Text('Kesimpulan Saran')
    keputusan_siswa = fields.Text('Keputusan')

    # Tanda Tangan
    ttd_ortu = fields.Text('Orang Tua / Wali')
    ttd_walas = fields.Text('Wali Kelas')
    ttd_kepsek = fields.Text('Kepala Sekolah')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('publish', 'Publish'),
        ('cancel', 'Cancel'),
    ], string='State', readonly=True, default='draft', required=True, tracking=True)


    
    def copy(self, default=None):
        if default is None:
            default = {}

        default.update({
            'kode_seq': self.env['ir.sequence'].next_by_code('raport.siswa.sts'),
            'raport_siswa_ids': [],  # Clear existing records if not supposed to duplicate
            'mulok_siswa_ids': [],   # Clear existing records if not supposed to duplicate
            'prestasi_siswa_ids': [],  # Clear existing records if not supposed to duplicate
        })

        # Add new records to default
        default['raport_siswa_ids'] = [(0, 0, {
            'subject_id': line.subject_id.id,
            'nilai_akhir': line.nilai_akhir,
            'note': line.note,
            'note2': line.note2,
        }) for line in self.raport_siswa_ids]

        default['mulok_siswa_ids'] = [(0, 0, {
            'student_id': line.student_id.id,
            'subject_id': line.subject_id.id,
            'nis_nisn': line.nis_nisn,
            'semester_id': line.semester_id,
            'tahun_pelajaran': line.tahun_pelajaran.id,
            'nilai_akhir': line.nilai_akhir,
            'note': line.note,
            'note2': line.note2,
        }) for line in self.mulok_siswa_ids]


        # default['prestasi_siswa_ids'] = [(0, 0, {
        #     'nama' : line.nama,
        #     'student_id': line.student_id.id,
        #     'nis_nisn': line.nis_nisn,
        #     'instansi': line.instansi,
        #     'url': line.url,
        #     'semester_id': line.semester_id,
        #     'tahun_pelajaran': line.tahun_pelajaran.id,
        #     'note': line.note,
        # }) for line in self.prestasi_siswa_ids]

        return super(RaportSiswaSTS, self).copy(default)
    
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['raport.siswa.sts'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'raport.siswa.sts',
            'docs': docs,
        }

    @api.model
    def get_report_sts_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport STS_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    @api.model
    def get_report_sas_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport SAS_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    @api.model
    def get_report_sat_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport SAT_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
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
     
     
    @api.model
    def get_current_date(self):
        translations = {
            'January': 'Januari',
            'February': 'Februari',
            'March': 'Maret',
            'April': 'April',
            'May': 'Mei',
            'June': 'Juni',
            'July': 'Juli',
            'August': 'Agustus',
            'September': 'September',
            'October': 'Oktober',
            'November': 'November',
            'December': 'Desember'
        }
        
        current_date = time.strftime('%d %B %Y')
        month_name = time.strftime('%B')
        translated_month = translations.get(month_name, '')
        
        return "{}".format(current_date.replace(month_name, translated_month))

    # @api.model
    # def create(self, vals):
    #     vals['kode_seq'] = self.env['ir.sequence'].next_by_code('raport.siswa.sts') or 'RAP/STS/'
    #     msg_body = 'Raport created'
    #     for msg in self:
    #         msg.message_post(body=msg_body)
    #     result = super(RaportSiswaSTS, self).create(vals)
    #     return result

class RaportSiswaLine(models.Model):
    _name = "raport.siswa.line"
    _description = "Raport Siswa Line"

    raport_id = fields.Many2one('raport.siswa.sts')
    subject_id = fields.Many2one('op.subject', 'Mata Pelajaran')
    nilai_akhir = fields.Integer('Nilai Akhir', size=8)
    note = fields.Text('Capaian Kompetensi', size=8)
    note2 = fields.Text('Catatan Kompetensi', size=8)
    
class KegiatanSiswa(models.Model):
    _name = "raport.siswa.kegiatan"
    _description = "Raport Siswa Line"

    raport_id = fields.Many2one('raport.siswa.sts')
    nama = fields.Text('Nama Kegiatan', size=8)
    deskripsi = fields.Text('Deskripsi Kegiatan', size=8)
    

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
            
            
class OpStudentPriodik(models.Model):
    _inherit = "op.student.priodik"  # Do not inherit mail.thread and mail.activity.mixin again

    raport_id = fields.Many2one('raport.siswa.sts')

class OpStudentMulok(models.Model):
    _inherit = "op.student.mulok"  # Do not inherit mail.thread and mail.activity.mixin again

    raport_id = fields.Many2one('raport.siswa.sts')

class OpStudentPrestasi(models.Model):
    _inherit = "op.student.prestasi"  # Do not inherit mail.thread and mail.activity.mixin again
    url = fields.Char('url')

    raport_id = fields.Many2one('raport.siswa.sts')
    