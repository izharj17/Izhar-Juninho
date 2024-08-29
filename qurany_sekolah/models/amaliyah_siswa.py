from odoo import models, fields, api
import datetime

class AmaliyahSiswa(models.Model):
    _name = "amaliyah.siswa"
    _description = "Amaliyah Siswa"
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
    amaliyah_siswa_salat_ids = fields.One2many('amaliyah.siswa.salat', 'salat_id', 'Praktik Salat')
    amaliyah_siswa_wudu_ids = fields.One2many('amaliyah.siswa.wudu', 'wudu_id', 'Praktik Wudu')
    amaliyah_siswa_haji_ids = fields.One2many('amaliyah.siswa.haji', 'haji_id', 'Praktik Haji')
    amaliyah_siswa_infaq_ids = fields.One2many('amaliyah.siswa.infaq', 'infaq_id', 'Infaq / Sedekah')
    
    @api.model
    def get_report_sts_filename(self):
        # Assuming `self` is a single record
        filename = 'Laporan Amaliyah _ {} _ {}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
    
class AmaliyahSiswaSalat(models.Model):
    _name = "amaliyah.siswa.salat"
    _description = "Amaliyah Siswa Salat"
    
    salat_id = fields.Many2one('amaliyah.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Guru', tracking=True)
    tanggal_salat = fields.Date('Tanggal Praktik', required=True, default=lambda self: fields.Date.today(), tracking=True)
    jenis_praktik = fields.Selection([
        ('bc' , 'Bacaan Salat'),
        ('gr' , 'Gerakan Salat'),
        ('zs' , 'Zikir Salat'),
    ], 'Jenis Praktik')    
    status = fields.Selection([
        ('a' , 'Sangat Baik'),
        ('b' , 'Baik'),
        ('c' , 'Cukup Baik'),
        ('d' , 'Perlu Perbaikan'),
    ], 'Status (حالة)')
    ketuntasan = fields.Boolean('Tuntas (مكتمل)')
    catatan = fields.Text('Catatan')

class AmaliyahSiswaWudu(models.Model):
    _name = "amaliyah.siswa.wudu"
    _description = "Amaliyah Siswa Wudu"
    
    wudu_id = fields.Many2one('amaliyah.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Guru', tracking=True)
    tanggal_wudu = fields.Date('Tanggal Praktik', required=True, default=lambda self: fields.Date.today(), tracking=True)
    jenis_praktik = fields.Selection([
        ('bw' , 'Bacaan Wudu'),
        ('gw' , 'Gerakan Wudu'),
        ('dw' , 'Doa Wudu'),
    ], 'Jenis Praktik')    
    status = fields.Selection([
        ('a' , 'Sangat Baik'),
        ('b' , 'Baik'),
        ('c' , 'Cukup Baik'),
        ('d' , 'Perlu Perbaikan'),
    ], 'Status (حالة)')
    ketuntasan = fields.Boolean('Tuntas (مكتمل)')
    catatan = fields.Text('Catatan')
    
class AmaliyahSiswaHaji(models.Model):
    _name = "amaliyah.siswa.haji"
    _description = "Amaliyah Siswa Haji"
    
    haji_id = fields.Many2one('amaliyah.siswa')
    guru_id = fields.Many2one('op.faculty', 'Nama Guru', tracking=True)
    tanggal_haji = fields.Date('Tanggal Praktik', required=True, default=lambda self: fields.Date.today(), tracking=True)
    jenis_praktik = fields.Selection([
        ('bh' , 'Bacaan Manasik Haji'),
        ('gh' , 'Gerakan Manasik Haji'),
    ], 'Jenis Praktik')    
    status = fields.Selection([
        ('a' , 'Sangat Baik'),
        ('b' , 'Baik'),
        ('c' , 'Cukup Baik'),
        ('d' , 'Perlu Perbaikan'),
    ], 'Status (حالة)')
    ketuntasan = fields.Boolean('Tuntas (مكتمل)')
    catatan = fields.Text('Catatan')
    
class AmaliyahSiswaInfaq(models.Model):
    _name = "amaliyah.siswa.infaq"
    _description = "Amaliyah Siswa Infaq"
    
    infaq_id = fields.Many2one('amaliyah.siswa')
    tanggal_infaq = fields.Date('Tanggal Infaq', required=True, default=lambda self: fields.Date.today(), tracking=True)
    nom_infaq = fields.Float('Nominal Infaq (Rp)')
    ketuntasan = fields.Boolean('Tuntas (مكتمل)')
    catatan = fields.Text('Catatan')