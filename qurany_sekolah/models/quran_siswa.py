from odoo import models, fields, api
import datetime

class QuranSiswa(models.Model):
    _name = "quran.siswa"
    _description = "Quran Siswa"
    _rec_name = "student_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    student_id = fields.Many2one('op.student', 'Nama Peserta Didik')
    nis_nisn = fields.Char('NIS/NISN', related='student_id.nisn')
    unit = fields.Selection([
        ('tk', 'TK'),
        ('sd', 'SD'),
        ('sm', 'SM'),      
        ],'Unit')
    kelas_id = fields.Many2one('op.course', 'Kelas', related='student_id.grade')
    rombel_id = fields.Many2one('op.batch', 'Rombel', related='student_id.rombel')
    semester_id = fields.Selection([
        ('ganjil', 'Ganjil'),
        ('genap', 'Genap'),
    ], 'Semester')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Pelajaran')
    quran_siswa_line_ids = fields.One2many('quran.siswa.line', 'hafalan_id', 'Tahfidz')
    quran_siswa_tahsin_ids = fields.One2many('quran.siswa.tahsin', 'hafalan_id', 'Tahsin')
    quran_siswa_hadist_ids = fields.One2many('quran.siswa.hadist', 'hadist_id', 'Hadist')
    quran_siswa_doa_ids = fields.One2many('quran.siswa.doa', 'doa_id', 'Doa Siswa')
    quran_siswa_tilawati_ids = fields.One2many('quran.siswa.tilawati', 'tilawati_id', 'Tilawati')
    
    @api.model
    def get_report_sts_filename(self):
        # Assuming `self` is a single record
        filename = 'Laporan Quran_{}_{}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['quran.siswa'].browse(docids)
        company_name = self.env.context.get('company_name', self.env.company.name)
        company_address = self.env.context.get('company_address', self.env.company.street)
        
        return {
            'doc_ids': docids,
            'doc_model': 'quran.siswa',
            'docs': docs,
            'company_name': company_name,
            'company_address': company_address,
        }
    
class QuranSiswaLine(models.Model):
    _name = "quran.siswa.line"
    _description = "Quran Siswa Line"
    
    hafalan_id = fields.Many2one('quran.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Guru', tracking=True)
    tanggal_hafalan = fields.Date('Tanggal Tahfidz', required=True, default=lambda self: fields.Date.today(), tracking=True)
    surah_id = fields.Many2one('master.surah', 'Nama Surah (سورة)', tracking=True)
    ayat = fields.Char('Jumlah Ayat (آية)', related='surah_id.ayat')
    juz_id = fields.Many2one('master.juz', 'Juz (جوز)')
    status = fields.Selection([
        ('a' , 'Sangat Baik'),
        ('b' , 'Baik'),
        ('c' , 'Cukup Baik'),
        ('d' , 'Perlu Perbaikan'),
    ], 'Status (حالة)')
    ketuntasan = fields.Boolean('Tuntas (مكتمل)')
    capaian = fields.Char('Capaian Hafalan')
    catatan = fields.Text('Catatan')
    
class QuranSiswaTahsin(models.Model):
    _name = "quran.siswa.tahsin"
    _description = "Quran Siswa Tahsin"
    
    hafalan_id = fields.Many2one('quran.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Penahsin', tracking=True)
    tanggal_tahsin = fields.Date('Tanggal Tahsin', required=True, default=lambda self: fields.Date.today(), tracking=True)
    surah_id = fields.Many2one('master.surah', 'Nama Surah (سورة)', tracking=True)
    ayat = fields.Char('Jumlah Ayat (آية)', related='surah_id.ayat')
    juz_id = fields.Many2one('master.juz', 'Juz (جوز)')
    status = fields.Selection([
        ('a' , 'Sangat Baik'),
        ('b' , 'Baik'),
        ('c' , 'Cukup Baik'),
        ('d' , 'Perlu Perbaikan'),
    ], 'Status (حالة)')
    catatan = fields.Text('Catatan')
    
class QuranSiswaHadist(models.Model):
    _name = "quran.siswa.hadist"
    _description = "Quran Siswa Hadist"
    
    hadist_id = fields.Many2one('quran.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Guru', tracking=True)
    tanggal_hadist = fields.Date('Tanggal Hafalan Hadist', required=True, default=lambda self: fields.Date.today(), tracking=True)
    nama_hadist = fields.Char('Nama Hadist')
    status = fields.Selection([
        ('l' , 'Lancar'),
        ('cl' , 'Cukup Lancar'),
        ('tl' , 'Tidak Lancar'),
    ], 'Status')
    ketuntasan = fields.Boolean('Tuntas')
    catatan = fields.Text('Catatan')
    
class QuranSiswaDoa(models.Model):
    _name = "quran.siswa.doa"
    _description = "Quran Siswa Doa"
    
    doa_id = fields.Many2one('quran.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Guru', tracking=True)
    tanggal_doa = fields.Date('Tanggal Hafalan Doa', required=True, default=lambda self: fields.Date.today(), tracking=True)
    nama_doa = fields.Char('Nama Doa')
    status = fields.Selection([
        ('l' , 'Lancar'),
        ('cl' , 'Cukup Lancar'),
        ('tl' , 'Tidak Lancar'),
    ], 'Status')
    ketuntasan = fields.Boolean('Tuntas')
    catatan = fields.Text('Catatan')
    
class QuranSiswaTilawati(models.Model):
    _name = "quran.siswa.tilawati"
    _description = "Quran Siswa Tilawati"
    
    tilawati_id = fields.Many2one('quran.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Mentor', tracking=True)
    tanggal_tilawati = fields.Date('Tanggal Tilawati', required=True, default=lambda self: fields.Date.today(), tracking=True)
    jilid = fields.Selection([
        ('jld_1', 'Jilid 1'),
        ('jld_2', 'Jilid 2'),
        ('jld_3', 'Jilid 3'),
        ('jld_4', 'Jilid 4'),
        ('jld_5', 'Jilid 5'),
        ('jld_6', 'Jilid 6'),
    ],'Jilid Tilawati')
    halaman = fields.Char('Capaian Tilawati')
    status = fields.Selection([
        ('l' , 'Lancar'),
        ('cl' , 'Cukup Lancar'),
        ('tl' , 'Tidak Lancar'),
    ], 'Status')
    ketuntasan = fields.Boolean('Tuntas')
    catatan = fields.Text('Catatan')