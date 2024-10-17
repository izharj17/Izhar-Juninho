from odoo import models, fields, api, _

class OpDataParent(models.Model):
    _name = "op.data.parent"
    _description = "Data Ayah"


class OpDataAyah(models.Model):
    _name = "op.data.ayah"
    _description = "Data Ayah"
    _rec_name = 'name_ayah'

    name_ayah = fields.Char('Nama Ayah Kandung')
    nama_panggilan = fields.Char('Nama Panggilan')
    nik_ayah = fields.Integer('NIK Ayah')
    thn_lahir = fields.Date('Tahun Lahir')
    alamat = fields.Char('Alamat')
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
    pendidikan = fields.Selection([
        ('1', 'Tidak Sekolah'),
        ('2', 'Putus SD'),
        ('3', 'SD Sederajat'),
        ('4', 'SMP Sederajat'),
        ('5', 'SMA Sederajat'),
        ('6', 'D1'),
        ('7', 'D3'),
        ('8', 'S1'),
        ('9', 'S2'),
        ('10', 'S3'),
    ], string='Pendidikan')
    pekerjaan = fields.Selection([
        ('1', 'Tidak bekerja'),
        ('2', 'Nelayan'),
        ('3', 'Petani'),
        ('4', 'Peternak'),
        ('5', 'PNS/TNI/POLRI'),
        ('6', 'Karyawan Swasta'),
        ('7', 'Wiraswasta'),
        ('8', 'Wirausaha'),
        ('9', 'Buruh'),
        ('10', 'Pensiunan'),
    ], string='Pekerjaan')
    jabatan = fields.Char('Jabatan')
    peng_perbulan = fields.Selection([
        ('1', '< Rp. 500.000'),
        ('2', 'Rp. 500.000-Rp.999.999'),
        ('3', 'Rp. 1.000.000-Rp.1.999.999'),
        ('4', 'Rp.2.000.000-Rp.4.999.999'),
        ('5', 'Rp.5.000.000-Rp.20.000.000'),
        ('6', '> Rp.20.000.000'),
        ('7', 'Tidak Berpenghasilan'),
    ], string='Penghasilan bulanan')
    # alamat_kantor = fields.Char('Alamat Kantor / Perusahaan')
    no_wa = fields.Integer(string='No Whatsapp')
    # no_kantor = fields.Integer('Nomor Kantor')
    kondisi = fields.Selection([
        ('1', 'Masih Hidup'),
        ('2', 'Meninggal Dunia'),
    ], string="Kondisi Ayah")
    jum_tanggungan = fields.Integer('Jumlah Tanggungan')
    stts_pernikahan = fields.Selection([
        ('1', 'Menikah'),
        ('2', 'Bercerai'),
        ('3', 'Bercerai Mati'),
    ], string="Status Pernikahan")
    email = fields.Char('Email')
    active = fields.Boolean(default=True)
    relationship_id = fields.Many2one('op.parent.relationship',
                                      'Relation with Student')
    attachment = fields.Char('Attachment')
    student_ayah_ids = fields.One2many('op.student', 'ayah_id', 'Student')

class OpDataIbu(models.Model):
    _name = "op.data.ibu"
    _description = "Data Ibu"
    _rec_name = 'name_ibu'

    name_ibu = fields.Char('Nama Ibu Kandung')
    nama_panggilan = fields.Char('Nama Panggilan')
    nik_ibu = fields.Integer('NIK Ibu')
    thn_lahir = fields.Date('Tahun Lahir')
    alamat = fields.Char('Alamat')
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
    pendidikan = fields.Selection([
        ('1', 'Tidak Sekolah'),
        ('2', 'Putus SD'),
        ('3', 'SD Sederajat'),
        ('4', 'SMP Sederajat'),
        ('5', 'SMA Sederajat'),
        ('6', 'D1'),
        ('7', 'D3'),
        ('8', 'S1'),
        ('9', 'S2'),
        ('10', 'S3'),
    ], string='Pendidikan')
    pekerjaan = fields.Selection([
        ('1', 'Tidak bekerja'),
        ('2', 'Nelayan'),
        ('3', 'Petani'),
        ('4', 'Peternak'),
        ('5', 'PNS/TNI/POLRI'),
        ('6', 'Karyawan Swasta'),
        ('7', 'Wiraswasta'),
        ('8', 'Wirausaha'),
        ('9', 'Buruh'),
        ('10', 'Pensiunan'),
    ], string='Pekerjaan')
    jabatan = fields.Char('Jabatan')
    peng_perbulan = fields.Selection([
        ('1', '< Rp. 500.000'),
        ('2', 'Rp. 500.000-Rp.999.999'),
        ('3', 'Rp. 1.000.000-Rp.1.999.999'),
        ('4', 'Rp.2.000.000-Rp.4.999.999'),
        ('5', 'Rp.5.000.000-Rp.20.000.000'),
        ('6', '> Rp.20.000.000'),
        ('7', 'Tidak Berpenghasilan'),
    ], string='Penghasilan bulanan')
    # alamat_kantor = fields.Char('Alamat Kantor / Perusahaan')
    no_wa = fields.Integer(string='No Whatsapp')
    # no_kantor = fields.Integer('Nomor Kantor')
    kondisi = fields.Selection([
        ('1', 'Masih Hidup'),
        ('2', 'Meninggal Dunia'),
    ], string="Kondisi Ibu")
    jum_tanggungan = fields.Integer('Jumlah Tanggungan')
    stts_pernikahan = fields.Selection([
        ('1', 'Menikah'),
        ('2', 'Bercerai'),
        ('3', 'Bercerai Mati'),
    ], string="Status Pernikahan")
    email = fields.Char('Email')
    active = fields.Boolean(default=True)
    relationship_id = fields.Many2one('op.parent.relationship',
                                      'Relation with Student')
    attachment = fields.Char('Attachment')
    student_ibu_ids = fields.One2many('op.student', 'ibu_id', 'Student')

class OpDataWali(models.Model):
    _name = "op.data.wali"
    _description = "Data Wali"
    _rec_name = 'name_wali'

    name_wali = fields.Char('Nama Wali')
    nama_panggilan = fields.Char('Nama Panggilan')
    nik_wali = fields.Integer('NIK Wali')
    thn_lahir = fields.Date('Tahun Lahir')
    alamat = fields.Char('Alamat')
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
    pendidikan = fields.Selection([
        ('1', 'Tidak Sekolah'),
        ('2', 'Putus SD'),
        ('3', 'SD Sederajat'),
        ('4', 'SMP Sederajat'),
        ('5', 'SMA Sederajat'),
        ('6', 'D1'),
        ('7', 'D3'),
        ('8', 'S1'),
        ('9', 'S2'),
        ('10', 'S3'),
    ], string='Pendidikan')
    pekerjaan = fields.Selection([
        ('1', 'Tidak bekerja'),
        ('2', 'Nelayan'),
        ('3', 'Petani'),
        ('4', 'Peternak'),
        ('5', 'PNS/TNI/POLRI'),
        ('6', 'Karyawan Swasta'),
        ('7', 'Wiraswasta'),
        ('8', 'Wirausaha'),
        ('9', 'Buruh'),
        ('10', 'Pensiunan'),
    ], string='Pekerjaan')
    jabatan = fields.Char('Jabatan')
    peng_perbulan = fields.Selection([
        ('1', '< Rp. 500.000'),
        ('2', 'Rp. 500.000-Rp.999.999'),
        ('3', 'Rp. 1.000.000-Rp.1.999.999'),
        ('4', 'Rp.2.000.000-Rp.4.999.999'),
        ('5', 'Rp.5.000.000-Rp.20.000.000'),
        ('6', '> Rp.20.000.000'),
        ('7', 'Tidak Berpenghasilan'),
    ], string='Penghasilan bulanan')
    # alamat_kantor = fields.Char('Alamat Kantor / Perusahaan')
    no_wa = fields.Integer(string='No Whatsapp')
    # no_kantor = fields.Integer('Nomor Kantor')
    kondisi = fields.Selection([
        ('1', 'Masih Hidup'),
        ('2', 'Meninggal Dunia'),
    ], string="Kondisi Wali")
    jum_tanggungan = fields.Integer('Jumlah Tanggungan')
    stts_pernikahan = fields.Selection([
        ('1', 'Menikah'),
        ('2', 'Bercerai'),
        ('3', 'Bercerai Mati'),
    ], string="Status Pernikahan")
    email = fields.Char('Email')
    active = fields.Boolean(default=True)
    relationship_id = fields.Many2one('op.parent.relationship',
                                      'Relation with Student')
    attachment = fields.Char('Attachment')
    student_wali_ids = fields.One2many('op.student', 'wali_id', 'Student')
