import time
import datetime
from odoo import models, fields, api

class RaportKampungSawah(models.Model):
    _name = "raport.kampung.sawah"
    _description = "Raport Kampung Sawah"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit mail.thread and mail.activity.mixin here
    _rec_name = 'jenis_raport'

    kode_seq = fields.Char(string="Raport ID", readonly=True)
    jenis_raport = fields.Selection([
        ('K13SD6', 'K13 SD6'),
        ('SD1-5', 'SD 1-5'),
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

    #Sikap
    spiritual = fields.Text('Mandiri')
    sosial = fields.Text('Disiplin')
    
    #Tahfidz
    
    menulis = fields.Text('Menulis Al-Qur`an')
    membaca = fields.Text('Membaca Al-Qur`an')
    tahfiz = fields.Text('Tahfiz')
    
    #Leadership
    pra_leader = fields.Text('Pra Leadership Kids Camp')
    leader = fields.Text('Leadership Kids Camp')
    live_in = fields.Text('Live In')
    outbond = fields.Text('Outbond')
    panahan = fields.Text('Panahan')
    berenang = fields.Text('Berenang')
    tradisional = fields.Text('Permainan Tradisional')
    backpacker = fields.Text('Backpacker')
    
    #Bisnis
    market = fields.Text('Market Day')
    pra_magang = fields.Text('Pra Magang')
    magang = fields.Text('Magang')
    
    market_day1 = fields.Text('Market Day 1')
    market_day2 = fields.Text('Market Day 2')
    
    
    
    
    # Isi Raport
    raport_siswa_ids = fields.One2many('raport.kampung.sawah.line', 'raport_id', 'Raport Line')
    raport_siswa_ids_1_5 = fields.One2many('raport.kampung.sawah.line.15', 'raport_id', 'Raport Line')
    proyek_siswa_ids = fields.One2many('raport.kampung.sawah.proyek', 'raport_id', 'Proyek')
    
    eskul_siswa_ids = fields.One2many('raport.kampung.sawah.eskul', 'raport_id', 'Ekstrakurikuler')
    
    # Ketidakhadiran
    sakit = fields.Integer(string="Sakit")
    ijin = fields.Integer(string="Ijin")
    tanpa_ket = fields.Integer(string="Tanpa Keterangan")

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

        return super(RaportKampungSawah, self).copy(default)
    
    

    @api.model
    def get_report_SD6_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport SD6_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    @api.model
    def get_report_SD1_5_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport SD_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    @api.model
    def get_report_perilaku_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport Perilaku_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    
    @api.depends('student_id.course_detail_ids')
    def _compute_kelas_id(self):
        for record in self:
            # Ambil kelas dari course_detail_ids pertama (jika ada)
            course_detail = record.student_id.course_detail_ids and record.student_id.course_detail_ids[0]
            if course_detail:
                record.kelas_id = course_detail.course_id

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



class RaportKampungSawahLine(models.Model):
    _name = "raport.kampung.sawah.line"
    _description = "Raport Siswa Line"

    raport_id = fields.Many2one('raport.kampung.sawah')
    subject_id = fields.Many2one('op.subject', 'Mata Pelajaran')
    tahu_nilai = fields.Integer('Nilai Pengetahuan', size=8)
    tahu_predikat = fields.Char('Predikat', size = 3)
    tahu_deskripsi =fields.Text('Kompetensi Pengetahuan', size=8)

    terampil_nilai = fields.Integer('Nilai Keterampilan', size=8)
    terampil_predikat = fields.Char('Predikat', size = 3)
    terampil_deskripsi =fields.Text('Kompetensi Keterampilan', size=8)
    
class RaportKampungSawahLine1_5(models.Model):
    _name = "raport.kampung.sawah.line.15"
    _description = "Raport Siswa Line"

    raport_id = fields.Many2one('raport.kampung.sawah')
    subject_id = fields.Many2one('op.subject', 'Mata Pelajaran')
    nilai_akhir = fields.Integer('Nilai', size=8)
    capaian =fields.Text('Capaian Kompetensi', size=8)

class ProyekSiswa(models.Model):
    _name = "raport.kampung.sawah.proyek"
    _description = "Raport Proyek Line"

    raport_id = fields.Many2one('raport.kampung.sawah')
    jenis_proyek = fields.Selection([
        ('INDIVIDU', 'Proyek Individu'),
        ('KELAS', 'Proyek Kelas'),
    ], 'Jenis Proyek')
    nama = fields.Text('Judul Proyek', size=8)
    deskripsi = fields.Text('Keterangan', size=8)
    
class EkstrakurikulerSiswa(models.Model):
    _name = "raport.kampung.sawah.eskul"
    _description = "eskul Siswa Line"

    raport_id = fields.Many2one('raport.kampung.sawah')
    
    nama = fields.Text('Ekstrakurikuler', size=8)
    deskripsi = fields.Text('Kegiatan', size=8)
    
    
    
## INHERIT ------------------------------------------------------------------------------------------------------------------------------------------------    
    
class OpStudentInherit(models.Model):
    _inherit = "op.student"

    raport_ks_ids = fields.One2many('raport.kampung.sawah', 'student_id', string='Raport Kampung Sawah')
    
class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    raport_ks_ids = fields.One2many('raport.kampung.sawah', 'sekolah_id', string='Raport Kampung Sawah')
    
class OpCourseInherit(models.Model):
    _inherit = 'op.course'

    raport_ks_ids = fields.One2many('raport.kampung.sawah', 'kelas_id', string='Raport Kampung Sawah')
    
class OpBatchInherit(models.Model):
    _inherit = 'op.batch'

    raport_ks_ids = fields.One2many('raport.kampung.sawah', 'grade_id', string='Raport Kampung Sawah')
    
class OpAcademicYearInherit(models.Model):
    _inherit = 'op.academic.year'

    raport_ks_ids = fields.One2many('raport.kampung.sawah', 'tahun_pelajaran', string='Raport Kampung Sawah')