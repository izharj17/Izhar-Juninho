from odoo import models, fields, api
import datetime

class KegiatanRamadanSiswa(models.Model):
    _name = "kegiatan.ramadan.siswa"
    _description = "Kegiatan Ramadan Siswa"
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
    kegiatan_ramadan_siswa_line_ids = fields.One2many('kegiatan.ramadan.siswa.line', 'ramadan_id', 'Kegiatan Ramadan')
    
    @api.model
    def get_report_sts_filename(self):
        # Assuming `self` is a single record
        filename = 'Laporan Kegiatan Ramadhan _ {} _ {}'.format(self.student_id.name, datetime.datetime.now().strftime('%d-%m-%Y'))
        return filename
    
class KegiatanRamadanSiswaLine(models.Model):
    _name = "kegiatan.ramadan.siswa.line"
    _description = "Kegiatan Ramadan Siswa Line"
    
    ramadan_id = fields.Many2one('kegiatan.ramadan.siswa')
    nama_kegiatan = fields.Char('Nama Kegiatan')
    tanggal_kegiatan = fields.Date('Tanggal Kegiatan', required=True, default=lambda self: fields.Date.today(), tracking=True)
    ketuntasan = fields.Boolean('Tuntas (مكتمل)')
    catatan = fields.Text('Catatan')