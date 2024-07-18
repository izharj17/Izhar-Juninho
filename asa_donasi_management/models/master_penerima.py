from odoo import models, fields, api

class master_penerima(models.Model):
    _name = "master.penerima"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master penerima"
    _rec_name = 'nama_penerima'

    nama_penerima = fields.Char('Nama penerima')
    email = fields.Char(string='Email', compute='_compute_email', readonly=False, store=True, tracking=11)
    phone = fields.Char(string='Phone', compute='_compute_phone', readonly=False, store=True, tracking=12)
    gender = fields.Selection([
        ('l', 'Laki-Laki'),
        ('p', 'Perempuan'),
    ], string='Jenis Kelamin')
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    alamat = fields.Char('Alamat')
    rtw = fields.Char('RT / RW')
    kelurahan_id = fields.Many2one('wilayah.kelurahan', string='Kelurahan', track_visibility='onchange')
    kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan', track_visibility='onchange')
    kabkota_id = fields.Many2one('wilayah.kabkota', string='Kab / Kota', track_visibility='onchange')
    provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')
    kodepos = fields.Char(string='Kodepos', store=True, track_visibility='onchange')

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

    @api.model
    def create(self, values):
        # Buat objek res.partner
        partner_values = {
            'name': values.get('nama_penerima'),
            'email': values.get('email'),
            'phone': values.get('phone'),
        }
        partner = self.env['res.partner'].create(partner_values)

        # Tambahkan referensi partner ke penerima
        values['partner_id'] = partner.id
        return super(master_penerima, self).create(values)