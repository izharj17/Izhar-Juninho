import time
import datetime
from odoo import models, fields, api

class RaportKampungSawah(models.Model):
    _name = "raport.kampung.sawah.perilaku"
    _description = "Raport Kampung Sawah"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'student_id'

    kode_seq = fields.Char(string="Raport ID", readonly=True)

    # Identitas
    student_id = fields.Many2one('op.student', 'Student', tracking=True)
    nis_nisn = fields.Char('NIS/NISN', related='student_id.nis')
    sekolah_id = fields.Many2one('res.company', 'Sekolah', default=lambda self: self.env['res.company'].search([('name', '=', 'SD Islam Arrasyid')], limit=1).id)
    alamat_sekolah = fields.Char('Alamat Sekolah', related='sekolah_id.street')
    kelas_id = fields.Many2one('op.course', 'Kelas', readonly=False)
    grade_id = fields.Many2one('op.batch', 'Rombel')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Pelajaran')
    
    start_month = fields.Selection([
        ('JA', 'Januari'),
        ('FB', 'Februari'),
        ('MR', 'Maret'),
        ('AP', 'April'),
        ('ME', 'Mei'),
        ('JN', 'Juni'),
        ('JL', 'Juli'),
        ('AG', 'Agustus'),
        ('SP', 'September'),
        ('OK', 'Oktober'),
        ('NO', 'November'),
        ('DS', 'Desember'),
    ], string='Mulai Bulan', required=True)
    
    end_month = fields.Selection([
        ('JA', 'Januari'),
        ('FB', 'Februari'),
        ('MR', 'Maret'),
        ('AP', 'April'),
        ('ME', 'Mei'),
        ('JN', 'Juni'),
        ('JL', 'Juli'),
        ('AG', 'Agustus'),
        ('SP', 'September'),
        ('OK', 'Oktober'),
        ('NO', 'November'),
        ('DS', 'Desember'),
    ], string='Akhir Bulan', required=True)



    # Isi
    perilaku_siswa_ids_1 = fields.One2many('raport.kampung.sawah.perilaku.line.1', 'raport_id', 'Raport Perilaku')
    perilaku_siswa_ids_2 = fields.One2many('raport.kampung.sawah.perilaku.line.2', 'raport_id', 'Raport Perilaku')
    perilaku_siswa_ids_3 = fields.One2many('raport.kampung.sawah.perilaku.line.3', 'raport_id', 'Raport Perilaku')
    perilaku_siswa_ids_4 = fields.One2many('raport.kampung.sawah.perilaku.line.4', 'raport_id', 'Raport Perilaku')
    
    # Kesimpulan
    
    kesimpulan = fields.Text('Kesimpulan')

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

    @api.model
    def create(self, vals):
        # Create the new record
        record = super(RaportKampungSawah, self).create(vals)

        # Define the default records for perilaku_siswa_ids_1
        default_records_1 = [
            'Mengucap Salam pada saat datang',
            'Salam pada fasilitator',
            'Meletakkan sepatu pada tempatnya',
            'Meletakkan tas pada tempatnya',
            'Bertanggungjawab dengan jadwal piket',
            'Makan dan Minum dengan tangan kanan',
            'Merapikan perlengkapan sholat',
            'Bertanggung jawab dengan kebersihan kelas',
            'Membuang sampah sesuai kategorinya',
            'Bisa melakukan budaya antri',
            'Bertanggungjawab dengan kebersihan kamar mandi',
            'Terbiasa meletakkan barang-barang setelah dipakai',
            'Terbiasa menghabiskan makan siangnya',
            'Tidak Pilih-pilih makanan'
        ]

        # Define the default records for perilaku_siswa_ids_2
        default_records_2 = [
            'Bisa menyampaikan apa yang diinginkan kepada fasilitator atau orang dewasa di sekolah',
            'Bisa mengikuti instruksi dari guru kelas, guru pendamping atau orang dewasa di sekolah',
            'Kontak mata dengan teman sebaya atau dengan orang dewasa di sekolah',
            'Mampu mengungkapkan perasaannya kepada teman sebayanya dengan cara yang tepat',
            'Mampu mengungkapkan perasaannya kepada orang dewasa di sekolah dengan cara yang tepat',
            'Bisa berbagi dengan teman sebaya',
            'Bisa bekerjasama dengan teman sebaya',
            'Mampu memulai percakapan dengan teman sebaya',
            'Mau mendengarkan saat teman sebayanya berbicara',
            'Bisa fokus dengan kegiatannya ketika ada teman yang melakukan kegiatan di dekatnya/tidak mudah terdistrak',
            'Bisa aktif berkomunikasi dengan teman sebayanya',
            'Tidak agresif kepada teman sebayanya',
            'Punya inisiatif dalam menolong teman atau fasilitator'
        ]

        # Define the default records for perilaku_siswa_ids_3
        default_records_3 = [
            'Mampu memahami perasaannya dan nama rasanya (Senang, Marah, Sedih, dll)',
            'Bisa menyatakan ketidaknyamanannya kepada teman sebaya atau orang dewasa di sekolah',
            'Tidak terpancing ketika ada teman yang marah',
            'Mampu menahan amarah dengan cara yang tepat',
            'Mampu mengatasi masalah kecil dengan teman sebaya tanpa bantuan fasilitator',
            'Bisa menemukan strategi yang tepat saat menyelesaikan masalah dengan teman sebayanya',
            'Punya kesadaran pribadi ketika sedang mengalami masalah dengan teman sebaya atau orang dewasa di sekolah',
            'Punya kesadaran bahwa dirinya dapat memberikan pengaruh pada teman-temannya',
            'Bisa menyelesaikan masalah dengan teman sebaya dengan menggunakan solusi non agresif',
            'Bisa mengekspresikan perasaannya dengan cara yang tepat',
            'Menyadari bahwa ada tugas yang belum dikerjakan/barang yang tidak dibawa dan punya solusi atas masalahnya',
            'Tidak menangis ketika ada sesuatu yang membuatnya tidak nyaman',
            'Mampu berpikir positif dan bisa menyampaikan hal positif tentang dirinya pada orang lain',
            'Tidak menyalahkan oranglain ketika menemui masalah',
            'Bisa tumbuh empatinya kepada teman sebaya dan fasilitator'
        ]

        # Define the default records for perilaku_siswa_ids_4
        default_records_4 = [
            'Fokus dalam mengerjakan kegiatan kelas',
            'Bisa bekerjasama dalam kegiatan kelompok',
            'Mampu menyelesaikan pekerjaan sekolah dengan tepat waktu',
            'Tahu jadwal urutan kegiatan dari pagi sampai siang hari',
            'Bertanggungjawab dengan kegiatan pagi',
            'Terlibat aktif dalam proses kegiatan belajar mengajar di kelas',
            'Memahami dan bisa menjalankan aturan kelas',
            'Tidak menyela ketika fasilitator sedang berbicara atau teman sekelas sedang mendapat giliran berbicara',
            'Tahan diri untuk tidak berbicara sendiri atau ngobrol saat proses belajar mengajar berlangsung.',
            'Mampu mengerjakan tugas kelas tanpa pendampingan personal dari fasilitator',
            'Mau bertanya ketika menemui masalah dalam mengerjakan soal/ketika mengalami kesulitan',
            'Tidak mudah menyerah dalam mengerjakan tugas kelas',
            'Tidak mudah mengeluh ketika mengerjakan tugas kelas'
        ]

        # Create the default records for perilaku_siswa_ids_1
        for name in default_records_1:
            self.env['raport.kampung.sawah.perilaku.line.1'].create({
                'raport_id': record.id,
                'nama': name
            })

        # Create the default records for perilaku_siswa_ids_2
        for name in default_records_2:
            self.env['raport.kampung.sawah.perilaku.line.2'].create({
                'raport_id': record.id,
                'nama': name
            })

        # Create the default records for perilaku_siswa_ids_3
        for name in default_records_3:
            self.env['raport.kampung.sawah.perilaku.line.3'].create({
                'raport_id': record.id,
                'nama': name
            })

        # Create the default records for perilaku_siswa_ids_4
        for name in default_records_4:
            self.env['raport.kampung.sawah.perilaku.line.4'].create({
                'raport_id': record.id,
                'nama': name
            })

        return record

    @api.model
    def get_report_perilaku_filename(self):
        # Assuming `self` is a single record
        filename = 'Raport Perilaku_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename

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


## Line Class

class RaportKampungSawahPerilakuLine1(models.Model):
    _name = "raport.kampung.sawah.perilaku.line.1"
    _description = "Perkembangan Kemandirian Personal"

    raport_id = fields.Many2one('raport.kampung.sawah.perilaku')
    nama = fields.Char('Nama')
    
    SB = fields.Boolean(default=False)
    B = fields.Boolean(default=False)
    C = fields.Boolean(default=False)
    PD = fields.Boolean(default=False)
    
class RaportKampungSawahPerilakuLine2(models.Model):
    _name = "raport.kampung.sawah.perilaku.line.2"
    _description = "Perkembangan Perilaku Sosial"

    raport_id = fields.Many2one('raport.kampung.sawah.perilaku')
    nama = fields.Char('Nama')
    
    SB = fields.Boolean(default=False)
    B = fields.Boolean(default=False)
    C = fields.Boolean(default=False)
    PD = fields.Boolean(default=False)
    
class RaportKampungSawahPerilakuLine3(models.Model):
    _name = "raport.kampung.sawah.perilaku.line.3"
    _description = "Perkembangan Emosi dan Kemampuan Problem Solving"

    raport_id = fields.Many2one('raport.kampung.sawah.perilaku')
    nama = fields.Char('Nama')
    
    SB = fields.Boolean(default=False)
    B = fields.Boolean(default=False)
    C = fields.Boolean(default=False)
    PD = fields.Boolean(default=False)
    
class RaportKampungSawahPerilakuLine4(models.Model):
    _name = "raport.kampung.sawah.perilaku.line.4"
    _description = "Perkembangan Kemampuan Pada Kegiatan kelas"

    raport_id = fields.Many2one('raport.kampung.sawah.perilaku')
    nama = fields.Char('Nama')
    
    SB = fields.Boolean(default=False)
    B = fields.Boolean(default=False)
    C = fields.Boolean(default=False)
    PD = fields.Boolean(default=False)


    
## INHERIT ------------------------------------------------------------------------------------------------------------------------------------------------    
    
class OpStudentInherit(models.Model):
    _inherit = "op.student"

    raport_ks_ids = fields.One2many('raport.kampung.sawah.perilaku', 'student_id', string='Raport Kampung Sawah')
    
class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    raport_ks_ids = fields.One2many('raport.kampung.sawah.perilaku', 'sekolah_id', string='Raport Kampung Sawah')
    
class OpCourseInherit(models.Model):
    _inherit = 'op.course'

    raport_ks_ids = fields.One2many('raport.kampung.sawah.perilaku', 'kelas_id', string='Raport Kampung Sawah')
    
class OpBatchInherit(models.Model):
    _inherit = 'op.batch'

    raport_ks_ids = fields.One2many('raport.kampung.sawah.perilaku', 'grade_id', string='Raport Kampung Sawah')
    
class OpAcademicYearInherit(models.Model):
    _inherit = 'op.academic.year'

    raport_ks_ids = fields.One2many('raport.kampung.sawah.perilaku', 'tahun_pelajaran', string='Raport Kampung Sawah')