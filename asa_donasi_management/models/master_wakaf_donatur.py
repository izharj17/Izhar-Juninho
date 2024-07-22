from odoo import models, fields, api

class master_wakaf_donatur(models.Model):
    _name = "master.wakaf.donatur"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Wakaf Donatur"
    _rec_name = 'nama_wakaf_donatur'

    nama_wakaf_donatur = fields.Char('Nama Wakaf Donatur')
    email = fields.Char(string='Email', compute='_compute_email', readonly=False, store=True, tracking=11)
    phone = fields.Char(string='Phone', compute='_compute_phone', readonly=False, store=True, tracking=12)
    gender = fields.Selection([
        ('l', 'Laki-Laki'),
        ('p', 'Perempuan'),
    ], string='Jenis Kelamin')
    note = fields.Text('Note')
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    tipe_donatur_id = fields.Many2one('master.tipe.donatur', string='Tipe Donatur')
    kelurahan_id = fields.Many2one('wilayah.kelurahan', string='Kelurahan')
    kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan')
    kabkota_id = fields.Many2one('wilayah.kabkota', string='Kab / Kota')
    provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')

    @api.model
    def create(self, values):
        # Buat objek res.partner
        partner_values = {
            'name': values.get('nama_wakaf_donatur'),
            'email': values.get('email'),
            'phone': values.get('phone'),
            'tipe_donatur_id': values.get('tipe_donatur_id'),
        }
        partner = self.env['res.partner'].create(partner_values)

        # Tambahkan referensi partner ke donatur
        values['partner_id'] = partner.id
        return super(master_wakaf_donatur, self).create(values)