from odoo import models, fields


class RaportSiswa(models.Model):
    _name = "raport.siswa"
    _description = "Raport Siswa"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('op.student', 'Nama Peserta Didik')
    nis_nisn = fields.Char('NIS/NISN')
    sekolah_id = fields.Many2one('res.company', 'Sekolah')
    alamat_sekolah = fields.Char('Alamat Sekolah')
    kelas_id = fields.Many2one('op.course', 'Kelas')
    grade_id = fields.Many2one('op.batch', 'Fase')
    semester_id = fields.Selection([
        ('1', '1 (Ganjil)'),
        ('2', '2 (Genap)'),
    ], 'Semester')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Pelajaran')

#     # raport_siswa_ids = fields.One2many('raport.siswa.line', 'raport_id', 'Raport Line')
#     # mulok_siswa_ids = fields.One2many('op.student.mulok', 'raport_id', 'Mulok')
#     # karakter_siswa_ids = fields.One2many('op.student.karakter', 'raport_id', 'Karakter')
#     # # kegiatan_siswa_ids = fields.One2many('op.activity', 'student_id', 'Kegiatan')
#     # # kehadiran_siswa_ids = fields.One2many('op.attendance.register.siswa', 'raport_siswa_id', 'Kehadiran')
#     # perkembangan_siswa_ids = fields.One2many('op.student.priodik', 'raport_id', 'Priodik')
#     # prestasi_siswa_ids = fields.One2many('op.student.prestasi', 'raport_id', 'Prestasi')

# # class RaportSiswaline(models.Model):
# #     _name = "raport.siswa.line"
# #     _description = "Raport Siswa Line"

# #     raport_id = fields.Many2one('raport.siswa')
# #     subject_id = fields.Many2one('op.subject', 'Mata Pelajaran')
# #     nilai_akhir = fields.Integer('Nilai Akhir')
# #     note = fields.Text('Capaian Kompetensi')


# class OpStudentRaport(models.Model):
#     _inherit = "op.student"

#     raport_count = fields.Integer(compute='compute_count_raport')

#     def get_raport(self):
#         action = self.env.ref('openeducat_core.'
#                               'raport_siswa_action').read()[0]
#         action['domain'] = [('student_id', 'in', self.ids)]
#         return action

#     def compute_count_raport(self):
#         for record in self:
#             record.raport_count = self.env['raport.siswa'].search_count(
#                 [('student_id', '=', self.id)])