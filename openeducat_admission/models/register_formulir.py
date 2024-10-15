from odoo import models, fields, api, _

class OpFormulir(models.Model):
    _name = "op.formulir"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Formulir"
    _rec_name = 'formulir'
    _order = 'id DESC'

    formulir = fields.Char('Nama Formulir')
    ppdb_id = fields.Many2one('op.admission.register', 'PPDB')
    product_id = fields.Many2one('product.product', 'Produk')
    date_begin = fields.Datetime(string='Start Date', required=True, tracking=True)
    date_end = fields.Datetime(string='End Date', required=True, tracking=True)
    register_formulir_ids = fields.One2many('op.register.formulir', 'formulir_id', string='Register Formulir',)

class OpRegisterParent(models.Model):
    _name = "op.register.parent"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Register Parent"
    _order = 'id DESC'
    _rec_name = 'nama_ortu'

    formulir_id = fields.Many2one('op.formulir', 'Formulir')
    ppdb_id = fields.Many2one('op.admission.register', 'PPDB', related='formulir_id.ppdb_id')
    product_id = fields.Many2one('product.product', 'Produk', related='formulir_id.product_id')
    price = fields.Float('Harga')
    qty = fields.Integer('Qty', default=1)
    nama_ortu = fields.Char('Nama Ortu')
    phone = fields.Char('No Whatsapp')
    email = fields.Char('Email')
    is_parent = fields.Boolean('Is a Parent', default=True)
    partner_id = fields.Many2one('res.partner', 'Partner', store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.list_price

    # @api.model
    # def create(self, values):
    #     # Buat record OpRegisterParent
    #     parent_record = super(OpRegisterParent, self).create(values)
    #
    #     # Buat record OpRegisterFormulir terkait dengan OpRegisterParent
    #     formulir_values = {
    #         'formulir_id': parent_record.formulir_id.id,
    #         'parent_id': parent_record.id,
    #         'product_id': parent_record.product_id.id,
    #         'price': parent_record.price,
    #         'qty': parent_record.qty,
    #         'date': fields.Datetime.now(),
    #         # Tambahkan field lain yang diperlukan
    #     }
    #     formulir_record = self.env['op.register.formulir'].create(formulir_values)
    #
    #     # Buat record res.partner
    #     partner_values = {
    #         'name': values.get('nama_ortu'),
    #         'email': values.get('email'),
    #         'phone': values.get('phone'),
    #         'is_parent': values.get('is_parent'),
    #     }
    #     partner = self.env['res.partner'].create(partner_values)
    #
    #     # Setel partner_id di OpRegisterParent dan OpRegisterFormulir
    #     parent_record.write({'partner_id': partner.id})
    #     formulir_record.write({'partner_id': partner.id})
    #
    #     return parent_record


class OpRegisterFormulir(models.Model):
    _name = "op.register.formulir"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Register Formulir"
    _order = 'id DESC'
    _rec_name = 'formulir_id'

    formulir_id = fields.Many2one('op.formulir', 'Formulir')
    ppdb_id = fields.Many2one('op.admission.register', 'PPDB')
    product_id = fields.Many2one('product.product', 'Produk')
    date = fields.Datetime('Tanggal')
    parent_id = fields.Many2one('op.register.parent', 'Parent')
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=False)
    qty = fields.Integer('Qty', default=1)
    price = fields.Float('Harga')
    total_price = fields.Float('Total Harga', compute='_compute_total_price')
    note = fields.Char('Keterangan')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    customer_invoice_id = fields.Many2one('account.invoice', 'Customer Invoice', readonly=True)

    @api.depends('price', 'qty')
    def _compute_total_price(self):
        for jumlah in self:
            penjumlahan = jumlah.qty * jumlah.price
            jumlah.total_price = penjumlahan

    @api.model
    def create_sale_order_and_invoice(self, record):
        # Panggil metode create dari model induk untuk membuat record
        record = super(OpRegisterFormulir, self).create(record)

        # Buat Sale Order secara otomatis saat formulir dibuat
        sale_order = self.env['sale.order'].create({
            'partner_id': record.partner_id.id,
            'date_order': record.date,
            'formulir_id': record.formulir_id.id,
            # Tambahkan produk dan informasi lainnya sesuai kebutuhan
            # Pastikan untuk menyesuaikan dengan pola bisnis Anda
        })

        # Tambahkan line order berdasarkan formulir yang baru dibuat
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': record.product_id.id,
            'product_uom_qty': record.qty,
            'price_unit': record.price,
            'name': record.note,
            # Tambahkan informasi lainnya sesuai kebutuhan
        })

        # Hubungkan Sale Order ke Formulir
        record.write({'sale_order_id': sale_order.id})

        # Setujui Sale Order secara otomatis
        sale_order.action_confirm()

        # Buat Faktur Pelanggan saat Sale Order dikonfirmasi
        customer_invoice = sale_order._create_invoices()

        # Hubungkan Faktur Pelanggan ke Formulir
        record.write({'customer_invoice_id': customer_invoice.id})

        if customer_invoice:
            customer_invoice.action_post()
            customer_invoice.write({'formulir_id': record.formulir_id.id})

        return record

class OpRegisterTransaksiLine(models.Model):
    _name = "op.register.transaksi.line"
    _description = "Register Transaksi Formulir"
    _order = 'id DESC'

    register_formulir_id = fields.Many2one('op.register.formulir', 'Register Formulir')
    note = fields.Char('Keterangan')
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    product_id = fields.Many2one('product.product', 'Produk')
    qty = fields.Integer('Qty', default=1)
    price = fields.Float('Harga')
    total_price = fields.Float('Total Harga', compute='_compute_total_price')

    @api.depends('price', 'qty')
    def _compute_total_price(self):
        for jumlah in self:
            penjumlahan = jumlah.qty * jumlah.price
            jumlah.total_price = penjumlahan

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.list_price

