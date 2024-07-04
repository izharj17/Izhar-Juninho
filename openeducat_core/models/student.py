# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date,datetime
from dateutil.relativedelta import relativedelta


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student', ondelete="cascade", tracking=True)
    course_id = fields.Many2one('op.course', 'Class', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', 'Rombel', required=True, tracking=True)
    roll_number = fields.Char('NIS', tracking=True)
    subject_ids = fields.Many2many('op.subject', string='Mata Pelajaran')
    academic_years_id = fields.Many2one('op.academic.year', 'Tahun Ajaran')
    academic_term_id = fields.Many2one('op.academic.term', 'Periode')
    state = fields.Selection([('running', 'Running'),
                              ('finished', 'Finished')],
                             string="Status", default="running")

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Student Course Details'),
            'template': '/openeducat_core/static/xls/op_student_course.xls'
        }]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    
    first_name = fields.Char('First Name', size=128, translate=True)
    middle_name = fields.Char('Middle Name', size=128, translate=True)
    last_name = fields.Char('Last Name', size=128, translate=True)
    grade = fields.Many2one('op.course', 'Grade')
    rombel = fields.Many2one('op.batch', 'Rombel')
    birth_date = fields.Date('Birth Date')
    age = fields.Char(compute='onchange_age', string="Usia", store=True)
    birth_place = fields.Char('Birth Place')
    nis = fields.Char('NIS')
    nisn = fields.Char('NISN')
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Gol. Darah')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Jenis Kelamin', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    gr_no = fields.Char("NIS", size=20)
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Course Details',
                                        tracking=True)
    active = fields.Boolean(default=True)
    ayah_id = fields.Many2one('op.data.ayah', 'Ayah')
    ibu_id = fields.Many2one('op.data.ibu', 'Ibu')
    wali_id = fields.Many2one('op.data.wali', 'Wali')
    barcode = fields.Char('Barcode')

    nama_panggilan = fields.Char('Nama Panggilan')
    no_kk = fields.Char('No KK')
    nik = fields.Char('NIK')
    no_akta_lahir = fields.Char('No Regsitrasi Akta Lahir')
    agama = fields.Selection([
        ('1', 'Islam'),
        ('2', 'Kristen'),
        ('3', 'Katolik'),
        ('4', 'Hindu'),
        ('5', 'Budha'),
    ], string='Agama')
    kewarganegaraan = fields.Selection([
        ('1', 'Indonesia (WNI)'),
        ('2', 'Asing (WNA)'),
    ], string="Kewarganegaraan")
    rt_rw = fields.Char('RT/RW')
    kecamatan_id = fields.Many2one('wilayah.kecamatan', 'Kecamatan')
    kelurahan_id = fields.Many2one('wilayah.kelurahan', 'Kelurahan')
    kode_pos = fields.Char('Kode POS')
    tempat_tinggal = fields.Selection([
        ('1', 'Bersama Orant Tua'),
        ('2', 'Wali'),
        ('3', 'Kos'),
        ('4', 'Asrama'),
        ('5', 'Panti Asuhan'),
    ], string='Tempat Tinggal')
    moda_transport = fields.Selection([
        ('1', 'Jalan Kaki'),
        ('2', 'Kendaraan Pribadi'),
        ('3', 'Kendaraan Umum/Angkot'),
        ('4', 'Jemputan Sekolah'),
        ('5', 'Kereta Api'),
        ('6', 'Ojek'),
        ('7', 'Lainnya'),
    ], string='Moda Transportasi')
    anak_ke = fields.Integer('Anak Ke')
    punya_kia = fields.Boolean('Apakah Punya KIA?')

    #Data Priodik
    tinggi_bdn = fields.Integer('Tinggi Badan')
    berat_bdn = fields.Integer('Berat Badan')
    lingkar_kpl = fields.Integer('Lingkar Kepala')
    jrk_tmpt_plhn = fields.Selection([
        ('1', 'Kurang dari 1 KM'),
        ('2', 'Lebih dari 1 KM'),
    ], string='Jarak Tempat Tinggal ke Sekolah')
    jrk_tmpt_km = fields.Integer('Jarak dalam KM')
    waktu_tempuh = fields.Integer('Waktu Tempuh')
    jmlh_saudara_kandung = fields.Integer('Jumlah Saudara Kandung')
    graduate = fields.Date('Waktu Kelulusan / Non-Aktif')
    status_graduasi = fields.Selection([
        ('1', 'Alumni'),
        ('2', 'Non-Aktif / Keluar'),
    ], 'Status Graduasi Siswa')

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    )]

    @api.depends('birth_date')
    def onchange_age(self):
        for rec in self:
            if rec.birth_date:
                d1 = rec.birth_date
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + "y" +" "+ str(rd.months) + "m" +" "+ str(rd.days) + "d"
            else:
                rec.age = "No Date Of Birth!!"

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name
            )
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id

class OpStudentPriodik(models.Model):
    _name = "op.student.priodik"
    _description = "Student Course Priodik"
    _inherit = "mail.thread"  # Inherited here
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student')
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

class OpStudentMulok(models.Model):
    _name = "op.student.mulok"
    _description = "Student Course Mulok"
    _inherit = "mail.thread"  # Inherited here
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student')
    subject_id = fields.Many2one('op.subject', 'Mata Pelajaran')
    nis_nisn = fields.Char('NIS/NISN')
    semester_id = fields.Selection([
        ('1', '1 (Ganjil)'),
        ('2', '2 (Genap)'),
    ], 'Semester')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Pelajaran')
    nilai_akhir = fields.Integer('Nilai Akhir')
    note = fields.Text('Capaian Kompetensi')
    note2 = fields.Text('Catatan Kompetensi')
    
    def add_follower(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id)
        if partner not in self.message_partner_ids:
            self.message_subscribe(partner_ids=partner_id)
        else:
            _logger.warning("Partner %s is already following this record.", partner.name)

class OpStudentKarakter(models.Model):
    _name = "op.student.karakter"
    _description = "Student Pilar Karakter"
    _inherit = "mail.thread"  # Inherited here
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Nama Siswa', ondelete="cascade", tracking=True)
    nis_nisn = fields.Char('NIS/NISN')
    sikap = fields.Selection([
        ('1', 'Tertib'),
        ('2', 'Mandiri'),
        ('3', 'Percaya Diri'),
        ('4', 'Disiplin'),
    ], 'Kategori Karakter')
    semester_id = fields.Selection([
        ('1', '1 (Ganjil)'),
        ('2', '2 (Genap)'),
    ], 'Semester')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Akademik')
    note = fields.Text('Deskripsi Karakter')
    
    def add_follower(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id)
        if partner not in self.message_partner_ids:
            self.message_subscribe(partner_ids=partner_id)
        else:
            _logger.warning("Partner %s is already following this record.", partner.name)

class OpStudentPrestasi(models.Model):
    _name = "op.student.prestasi"
    _description = "Student Pilar Prestasi"
    _inherit = "mail.thread"  # Inherited here
    _rec_name = 'student_id'

    nama = fields.Char('Nama')
    student_id = fields.Many2one('op.student', 'Nama Siswa', ondelete="cascade", tracking=True)
    nis_nisn = fields.Char('NISN')
    url = fields.Char('url')
    instansi = fields.Char('Nama Instansi')
    semester_id = fields.Selection([
        ('1', '1 (Ganjil)'),
        ('2', '2 (Genap)'),
    ], 'Semester')
    tahun_pelajaran = fields.Many2one('op.academic.year', 'Tahun Akademik')
    note = fields.Text('Catatan')

    def add_follower(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id)
        if partner not in self.message_partner_ids:
            self.message_subscribe(partner_ids=partner_id)
        else:
            _logger.warning("Partner %s is already following this record.", partner.name)