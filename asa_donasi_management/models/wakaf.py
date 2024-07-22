from odoo import models, fields, api

class wakaf_management(models.Model):
    _name = "wakaf.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Wakaf Management"
    _rec_name = 'nama_program'

    nama_program = fields.Char('Nama Program')
    program_wakaf_id = fields.Many2one('master.program.wakaf', 'Program Wakaf')
    category_wakaf_id = fields.Many2one('master.category.wakaf', 'Kategori Wakaf')
    tipe_wakaf_id = fields.Selection([
        ('wk', 'Wakaf Kolektif'),
        ('wa', 'Wakaf Abadi'),
        ('wb', 'Wakaf Berjangka'),
    ], string='Tipe Wakaf')
    keterangan = fields.Text('Keterangan')
    saldo = fields.Float('Saldo', compute='_compute_total_nilai_wakaf')
    tersalurkan = fields.Float('Realisasi', compute='_compute_total_nilai_realisasi')
    date_begin = fields.Datetime(string='Start Date', required=True, tracking=True)
    date_end = fields.Datetime(string='End Date', required=True, tracking=True)
    yayasan_id = fields.Many2one('res.partner', 'Yayasan')
    person_id = fields.Many2one('res.users', 'Create Person')
    wakaf_donatur_ids = fields.One2many('register.wakaf.donatur', 'wakaf_id', string='Wakaf Donatur',)
    target_terkumpul = fields.Float('Target Terkumpul', compute='_compute_target_terkumpul')
    progres_saldo_terkumpul = fields.Float('Progres Saldo Terkumpul', compute='_compute_progres_saldo_terkumpul', store=True)
    jumlah_donatur_wakaf = fields.Integer('Jumlah Donatur Wakaf', compute='_compute_jumlah_donatur_wakaf')
    product_id = fields.Many2one('product.product', 'Produk')
    qty = fields.Integer('Qty')
    nilai_rab = fields.Float('Nilai')
    total_rab = fields.Float('Total RAB', compute='_compute_total_rab')
    note = fields.Char('Note')
    rab_wakaf_ids = fields.One2many('rab.wakaf.line', 'wakaf_management_id', string='RAB Wakaf',)
    wakaf_realisasi_ids = fields.One2many('register.realisasi', 'realisasi_wakaf_id', string='Realisasi Wakaf', )

    @api.depends('total_rab', 'target_terkumpul')
    def _compute_target_terkumpul(self):
        for wakaf in self:
            wakaf.target_terkumpul = wakaf.total_rab

    @api.depends('wakaf_realisasi_ids.total_realisasi')
    def _compute_total_nilai_realisasi(self):
        for realisasi in self:
            total = sum(realisasi.wakaf_realisasi_ids.mapped('total_realisasi'))
            realisasi.tersalurkan = total

    @api.depends('rab_wakaf_ids.total')
    def _compute_total_rab(self):
        for record in self:
            jumlah_rab = sum(total_rab.total for total_rab in record.rab_wakaf_ids)
            record.total_rab = jumlah_rab

    @api.depends('nilai_rab', 'qty')
    def _compute_total_nilai_rab(self):
        for jumlah_rab in self:
            total = jumlah_rab.qty * jumlah_rab.nilai_rab
            jumlah_rab.total_rab = total

    @api.depends('wakaf_donatur_ids')
    def _compute_jumlah_donatur_wakaf(self):
        for record in self:
            record.jumlah_donatur_wakaf = len(record.wakaf_donatur_ids)

    @api.depends('wakaf_donatur_ids.nilai_wakaf')
    def _compute_total_nilai_wakaf(self):
        for wakaf in self:
            total = sum(wakaf.wakaf_donatur_ids.mapped('nilai_wakaf'))
            wakaf.saldo = total

    @api.depends('saldo', 'target_terkumpul')
    def _compute_progres_saldo_terkumpul(self):
        for record in self:
            if record.target_terkumpul > 0:
                progress = (record.saldo / record.target_terkumpul) * 100
                record.progres_saldo_terkumpul = min(100, progress)
            else:
                record.progres_saldo_terkumpul = 0

class register_wakaf_donatur(models.Model):
    _name = "register.wakaf.donatur"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Register Wakaf Donatur"
    _rec_name = 'wakaf_id'

    wakaf_id = fields.Many2one('wakaf.management', string='Wakaf', required=True, domain="[('tipe_wakaf_id', '=', tipe_wakaf_id)]")
    category_wakaf_id = fields.Many2one('master.category.wakaf', 'Kategori Wakaf')
    tipe_wakaf_id = fields.Selection([
        ('wk', 'Wakaf Kolektif'),
        ('wa', 'Wakaf Abadi'),
        ('wb', 'Wakaf Berjangka'),
    ], string='Tipe Wakaf')
    product_id = fields.Many2one('product.product', 'Produk')
    wakaf_donatur_id = fields.Many2one('master.wakaf.donatur', 'Donatur')
    email = fields.Char(string='Email', related='wakaf_donatur_id.email')
    phone = fields.Char(string='Phone', related='wakaf_donatur_id.phone')
    infaq_date = fields.Date('Tanggal Wakaf')
    nilai_wakaf = fields.Float('Nilai Wakaf')
    total_wakaf = fields.Float('Total Wakaf', compute='_compute_total_nilai_wakaf')
    note = fields.Char('Note', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner')
    qty = fields.Integer('Qty')
    jangka_waktu_wakaf = fields.Selection([
        ('pilih', '- Pilih Jangka Waktu Wakaf Berjangka'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ], 'Jangka Waktu', required=False)
    bank = fields.Char('Bank')
    cabang_bank = fields.Char('Cabang Bank')
    no_rek = fields.Integer('No Rekening')
    nama_pemilik_rek = fields.Char('Nama Pemilik Rekening')

    # wakaf_donatur_line_ids =fields.One2many('register.wakaf.donatur.line', 'wakaf_donatur_line_id', 'Wakaf Donatur Line')

    @api.depends('nilai_wakaf', 'qty')
    def _compute_total_nilai_wakaf(self):
        for jumlah_wakaf in self:
            total = jumlah_wakaf.qty * jumlah_wakaf.nilai_wakaf
            jumlah_wakaf.total_wakaf = total

    @api.onchange('wakaf_donatur_id')
    def _onchange_wakaf_donatur_id(self):
        if self.wakaf_donatur_id:
            self.partner_id = self.wakaf_donatur_id.partner_id

    @api.model_create_single
    def create(self, values):
        if 'wakaf_donatur_id' in values:
            donatur = self.env['master.wakaf.donatur'].browse(values['wakaf_donatur_id'])
            values['partner_id'] = donatur.partner_id.id
        self.create_sale_order(values)
        return super(register_wakaf_donatur, self).create(values)

    def create_sale_order(self, values):
        if 'product_id' in values:
            sale_order_obj = self.env['sale.order']
            sale_order_line_obj = self.env['sale.order.line']

            vals = {
                'partner_id': values['partner_id'],
                'date_order': values['infaq_date'],
                'wakaf_id': values['wakaf_id'],
            }
            sale_order = sale_order_obj.create(vals)
            sale_order.wakaf_id = values['wakaf_id']

            so_line_vals = {
                'product_id': values['product_id'],
                'name': values['note'],
                'price_unit': values['nilai_wakaf'],
                'product_uom_qty': 1,
                'order_id': sale_order.id,
            }
            sale_order_line = sale_order_line_obj.create(so_line_vals)

            # Membuat faktur pelanggan
            sale_order.action_confirm()  # Konfirmasi pesanan penjualan
            invoice = sale_order._create_invoices()

            if invoice:
                invoice.write({'state': 'draft'})
                # invoice.write({'wakaf_id': values['wakaf_id']})

        return True

class rab_wakaf_line(models.Model):
    _name = "rab.wakaf.line"
    _description = "RAB Wakaf Line"

    wakaf_management_id = fields.Many2one('wakaf.management', 'Wakaf Management')
    product_id = fields.Many2one('product.product', 'Produk')
    qty = fields.Integer('Qty', default=1)
    uom_id = fields.Many2one('uom.uom', 'Uom')
    deskripsi = fields.Char('Deskripsi')
    nilai = fields.Float('Nilai')
    total = fields.Float('Total', compute='_compute_total_nilai')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            # Isi uom_id dengan uom dari product_id
            self.uom_id = self.product_id.uom_id.id

    @api.depends('nilai', 'qty')
    def _compute_total_nilai(self):
        for jumlah in self:
            penjumlahan = jumlah.qty * jumlah.nilai
            jumlah.total = penjumlahan

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.list_price

class register_realisasi(models.Model):
    _name = "register.realisasi"
    _description = "Register Realisasi"

    realisasi_wakaf_id = fields.Many2one('wakaf.management')
    wakaf_id = fields.Many2one('wakaf.management', string='Wakaf', required=True)
    product_id = fields.Many2one('product.product', 'Produk')
    qty = fields.Integer('qty')
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    date = fields.Date('Tanggal Order')
    nilai_realisasi = fields.Float('Nilai Realisasi')
    note = fields.Char('Note')
    total_realisasi = fields.Float('Total', compute='_compute_total_nilai_realisasi')

    @api.depends('nilai_realisasi', 'qty')
    def _compute_total_nilai_realisasi(self):
        for jumlah in self:
            penjumlahan = jumlah.qty * jumlah.nilai_realisasi
            jumlah.total_realisasi = penjumlahan

    @api.model_create_single
    def create(self, values):
        if 'product_id' in values:
            product = self.env['product.product'].browse(values['product_id'])
            if product.type == 'product' and product.categ_id == 'product':
                # Produk adalah storable, buat proses penerimaan barang (Stock Picking)
                stock_picking = self.create_stock_picking(values)
                values['stock_picking_id'] = stock_picking.id

                # Validasi proses penerimaan barang
                stock_picking.button_validate()
                # Jalankan metode "process" atau "action_process" jika ada
                if hasattr(stock_picking, 'action_process'):
                    stock_picking.action_process()
                elif hasattr(stock_picking, 'process'):
                    stock_picking.process()

        self.create_purchase_order(values)
        return super(register_realisasi, self).create(values)

    def create_stock_picking(self, values):
        stock_picking_obj = self.env['stock.picking']
        stock_move_obj = self.env['stock.move']

        picking_type = self.env.ref('stock.picking_type_in')
        location_src = self.env.ref('stock.stock_location_suppliers')
        location_dest = self.env.ref('stock.stock_location_customers')

        vals = {
            'partner_id': values['partner_id'],
            'picking_type_id': picking_type.id,
            'location_id': location_src.id,
            'location_dest_id': location_dest.id,
            'scheduled_date': values['date'],
            'origin': values['note'],
            'wakaf_id': values['wakaf_id'],
        }
        stock_picking = stock_picking_obj.create(vals)

        move_vals = {
            'name': values['note'],
            'product_id': values['product_id'],
            'product_uom_qty': 1,
            'product_uom': values['product_id'].uom_id.id,
            'location_id': location_src.id,
            'location_dest_id': location_dest.id,
            'picking_id': stock_picking.id,
        }
        stock_move = stock_move_obj.create(move_vals)

        # Validasi proses penerimaan barang
        stock_picking.button_validate()

        return stock_picking

    def create_purchase_order(self, values):
        if 'product_id' in values:
            purchase_order_obj = self.env['purchase.order']
            purchase_order_line_obj = self.env['purchase.order.line']
            account_move_obj = self.env['account.move']

            vals = {
                'partner_id': values['vendor_id'],
                'date_order': values['date'],
                'wakaf_id': values['wakaf_id'],
            }
            purchase_order = purchase_order_obj.create(vals)
            purchase_order.wakaf_id = values['wakaf_id']

            po_line_vals = {
                'product_id': values['product_id'],
                'name': values['note'],
                'price_unit': values['nilai_realisasi'],
                'product_qty': values['qty'],
                'order_id': purchase_order.id,
            }
            purchase_order_line = purchase_order_line_obj.create(po_line_vals)

            # Membuat faktur pelanggan
            purchase_order.button_confirm()
            purchase_order.action_create_invoice()

            # Cari faktur pelanggan yang dibuat dari purchase order
            vendorbill = account_move_obj.search([('purchase_id', '=', purchase_order.id)])

            if vendorbill:
                vendorbill.write({'wakaf_id': values['wakaf_id']})

        return True


class master_program_wakaf(models.Model):
    _name = "master.program.wakaf"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Program Wakaf"
    _rec_name = 'nama_program_wakaf'

    nama_program_wakaf = fields.Char('Nama Program')
    code = fields.Char('Code')

class master_category_wakaf(models.Model):
    _name = "master.category.wakaf"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Category Wakaf"
    _rec_name = 'nama_category_wakaf'

    nama_category_wakaf = fields.Char('Nama Category')
    code = fields.Char('Code')

class master_tipe_wakaf(models.Model):
    _name = "master.tipe.wakaf"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Tipe Wakaf"
    _rec_name = 'nama_tipe_wakaf'

    nama_tipe_wakaf = fields.Char('Nama Tipe Wakaf')
    code = fields.Char('Code')