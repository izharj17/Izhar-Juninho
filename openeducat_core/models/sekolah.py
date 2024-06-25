from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProfileSekolah(models.Model):
    _name = "profile.sekolah"
    _description = "Profile Sekolah"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('First Name', size=128, translate=True)
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128, required=True)
    kepsek_id = fields.Char('Kepala Sekolah')
    operator_id = fields.Char('Operator')
    akreditasi = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C')
    ], 'Akreditasi', required=True)
    kurikulum = fields.Char('Kurikulum')
    waktu = fields.Char('Waktu')

    #profile
    #identitas
    npsn = fields.Integer('NPSN')
    status = fields.Selection([
        ('n', 'Negeri'),
        ('s', 'Swasta')
    ], 'Status', required=True)
    bentuk_pendidikan = fields.Selection([
        ('tk', 'TK'),
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('univ', 'Universitas')
    ], 'Bentuk Pendidikan', required=True)
    status_kepemilikan = fields.Selection([
        ('pd', 'Pemerintah Daerah'),
        ('perseorangn', 'Perseorangan')
    ], 'Status Kepemilikan', required=True)
    sk_pendirian = fields.Char('SK Pendirian Sekolah')
    tgl_sk_pendirian = fields.Date('Tanggal SK Pendirian')
    sk_izin_oprs = fields.Char('SK Izin Operasionan')
    tgl_sk_izin_oprs = fields.Date('Tanggal SK Izin Operasiopan')

    #data pelengkap
    keb_khusus_layanan = fields.Selection([
        ('ada', 'Ada'),
        ('tdk ada', 'Tidak Ada')
    ], 'Kebutuhan Khusus Dilayani')
    bank_id = fields.Many2one('res.bank', 'Nama Bank')
    cab_kcp = fields.Char('Cabang KCP/Unit')
    rek = fields.Char('Rekening Atas Nama')

    #Data Rinci
    status_bos = fields.Selection([
        ('bm', 'Bersedia Menerima'),
        ('tbm', 'Tidak Bersedia Menerima')
    ], 'Status BOS')
    waktu_penyelenggaraan = fields.Char('Waktu Penyelenggaraan')
    sertifikasi_iso = fields.Selection([
        ('s', 'Bersertifikat'),
        ('bs', 'Belum Bersertifikat')
    ], 'Sertifikasi ISO')
    sumber_listrik = fields.Selection([
        ('pln', 'PLN'),
        ('tdk ada', 'Tidak Ada')
    ], 'Sumber Listrik')
    daya_listerik = fields.Selection([
        ('a', '900'),
        ('b', '1300'),
        ('c', '2000'),
        ('d', '22000'),
    ], 'Daya Listerik')
    kec_internet = fields.Char('Kecepatan Internet')

    #Rekapitulasi
    teacher_ids = fields.One2many('op.faculty', 'sekolah_id', 'Guru')
    student_ids = fields.One2many('op.student', 'sekolah_id', 'Peserta Didik')

    # id_number = fields.Char('ID Card Number', size=64)
    # login = fields.Char(
    #     'Login', related='partner_id.user_id.login', readonly=1)
    # last_login = fields.Datetime('Latest Connection', readonly=1,
    #                              related='partner_id.user_id.login_date')
    active = fields.Boolean(default=True)

    guru_count = fields.Integer(compute='_compute_guru_count', string='Jumlah Guru')
    tendik_count = fields.Integer(compute='_compute_tendik_count', string='Jumlah Tendik')
    total_count = fields.Integer(compute='_compute_total_count', string='Jumlah PTK')
    pd_count = fields.Integer(compute='_compute_student_count', string='Jumlah PD')

    yayasan_id = fields.Many2one('master.yayasan', 'Yayasan')

    #Kontak
    alamat = fields.Char('Alamat')
    rtw = fields.Char('RT / RW')
    dusun_id = fields.Char('Dusun')
    kelurahan_id = fields.Many2one('wilayah.kelurahan', string='Kelurahan', track_visibility='onchange')
    kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan', track_visibility='onchange')
    kabkota_id = fields.Many2one('wilayah.kabkota', string='Kab / Kota', track_visibility='onchange')
    provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')
    region_id = fields.Many2one('master.region', 'Region')
    kodepos = fields.Char(string='Kodepos', store=True, track_visibility='onchange')
    lintang = fields.Integer('Lintang')
    bujur = fields.Integer('Bujur')

    @api.onchange('region_id')
    def _onchange_region_id(self):
        if self.region_id:
            prov = self.env['wilayah.provinsi'].search([('region_id', '=', self.region_id.id)])
            return {'domain': {'provinsi_id': [('id', 'in', prov.ids)]}}

    @api.onchange('provinsi_id')
    def _onchange_provinsi_id(self):
        if self.provinsi_id:
            kabkota = self.env['wilayah.kabkota'].search([('provinsi_id', '=', self.provinsi_id.id)])
            return {'domain': {'kabkota_id': [('id', 'in', kabkota.ids)]}}

    @api.onchange('kabkota_id')
    def _onchange_kabkota_id(self):
        if self.kabkota_id:
            kecamatan = self.env['wilayah.kecamatan'].search([('kabkota_id', '=', self.kabkota_id.id)])
            return {'domain': {'kecamatan_id': [('id', 'in', kecamatan.ids)]}}

    @api.onchange('kecamatan_id')
    def _onchange_kecamatan_id(self):
        if self.kecamatan_id:
            kelurahan = self.env['wilayah.kelurahan'].search([('kecamatan_id', '=', self.kecamatan_id.id)])
            return {'domain': {'kelurahan_id': [('id', 'in', kelurahan.ids)]}}

    @api.onchange('kelurahan_id')
    def _onchange_kelurahan_id(self):
        if self.kelurahan_id:
            self.kodepos = self.kelurahan_id.kodepos

    @api.depends('teacher_ids.jenis_tenaga_kerja')
    def _compute_guru_count(self):
        for school in self:
            guru_count = len(school.teacher_ids.filtered(lambda teacher: teacher.jenis_tenaga_kerja == 'guru'))
            school.guru_count = guru_count

    @api.depends('teacher_ids.jenis_tenaga_kerja')
    def _compute_tendik_count(self):
        for school in self:
            tendik_count = len(school.teacher_ids.filtered(lambda teacher: teacher.jenis_tenaga_kerja == 'tendik'))
            school.tendik_count = tendik_count

    @api.depends('guru_count', 'tendik_count')
    def _compute_total_count(self):
        for school in self:
            school.total_count = school.guru_count + school.tendik_count

    @api.depends('student_ids')
    def _compute_student_count(self):
        for school in self:
            pd_count = len(school.student_ids)
            school.pd_count = pd_count

    #Data Sarpras
    sarpras_ids = fields.One2many('data.sarpras', 'sekolah_id', 'Data Sarpras')

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name)
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    # Data Sarpras
    sanitasi_ids = fields.One2many('data.sanitasi', 'sekolah_id', 'Data Sanitasi')

    # Data Rombel
    rombel_ids = fields.One2many('data.rombel', 'sekolah_id', 'Data Rombel')

    # def create_employee(self):
    #     for record in self:
    #         vals = {
    #             'name': record.name,
    #             'country_id': record.nationality.id,
    #             'gender': record.gender,
    #             'address_home_id': record.partner_id.id
    #         }
    #         emp_id = self.env['hr.employee'].create(vals)
    #         record.write({'emp_id': emp_id.id})
    #         record.partner_id.write({'partner_share': True, 'employee': True})

    # @api.model
    # def get_import_templates(self):
    #     return [{
    #         'label': _('Import Template for Faculties'),
    #         'template': '/openeducat_core/static/xls/op_faculty.xls'
    #     }]


class DataSarpras(models.Model):
    _name = "data.sarpras"
    _description = "Data Sarpras"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sekolah_id = fields.Many2one('profile.sekolah', 'Sekolah')
    jenis_sarpras_id = fields.Many2one('op.facility', 'Jenis Sarpras')
    semester = fields.Selection([
        ('ganjil', 'Ganjil'),
        ('genap', 'Genap')
    ], 'Semester')
    juml_ganjil = fields.Integer('Jumlah Ganjil')
    juml_genap = fields.Integer('Jumlah Genap')
    active = fields.Boolean(default=True)

class DataSanitasi(models.Model):
    _name = "data.sanitasi"
    _description = "Data Sanitasi"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sekolah_id = fields.Many2one('profile.sekolah', 'Sekolah')
    jenis_sanitasi_id = fields.Many2one('master.sanitasi', 'Nama Variabel')
    uraian = fields.Text('Uraian')
    active = fields.Boolean(default=True)

class DataRombel(models.Model):
    _name = "data.rombel"
    _description = "Data Rombel"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sekolah_id = fields.Many2one('profile.sekolah', 'Sekolah')
    rombel = fields.Text('Rombel')
    jenis_pendidikan = fields.Selection([
        ('tk', 'TK'),
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('univ', 'Universitas')
    ], 'Jenis Pendidikan', required=True)
    active = fields.Boolean(default=True)

