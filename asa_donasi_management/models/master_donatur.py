from odoo import models, fields, api

class master_donatur(models.Model):
    _name = "master.donatur"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Donatur"
    _rec_name = 'nama_donatur'

    nama_donatur = fields.Char('Nama Donatur')
    email = fields.Char(string='Email', compute='_compute_email', readonly=False, store=True, tracking=11)
    phone = fields.Char(string='Phone', compute='_compute_phone', readonly=False, store=True, tracking=12)
    gender = fields.Selection([
        ('l', 'Laki-Laki'),
        ('p', 'Perempuan'),
    ], string='Jenis Kelamin')
    note = fields.Text('Note')
    partner_id = fields.Many2one('res.partner', 'Partner')
    kelurahan_id = fields.Many2one('wilayah.kelurahan', string='Kelurahan')
    kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan')
    kabkota_id = fields.Many2one('wilayah.kabkota', string='Kab / Kota')
    provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')

    @api.model
    def create(self, values):
        # Cek apakah sudah ada partner dengan nama_donatur dan phone yang sama
        existing_partner = self.env['res.partner'].search([
            ('name', '=', values.get('nama_donatur')),
            ('phone', '=', values.get('phone')),
        ])

        if existing_partner:
            # Jika sudah ada, gunakan partner yang sudah ada
            values['partner_id'] = existing_partner.id
        else:
            # Jika belum ada, buat objek res.partner
            partner_values = {
                'name': values.get('nama_donatur'),
                'email': values.get('email'),
                'phone': values.get('phone'),
            }
            partner = self.env['res.partner'].create(partner_values)

            # Tambahkan referensi partner ke donatur
            values['partner_id'] = partner.id

        return super(master_donatur, self).create(values)

class master_tipe_donatur(models.Model):
    _name = "master.tipe.donatur"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Master Tipe Donatur"
    _rec_name = 'nama_tipe_donatur'

    nama_tipe_donatur = fields.Char('Tipe Donatur')