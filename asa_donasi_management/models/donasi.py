from odoo import models, fields, api

class donasi_management(models.Model):
    _name = "donasi.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Donasi Management"
    _rec_name = 'nama_program'

    nama_program = fields.Char('Nama Program')
    program_donasi_id = fields.Many2one('master.program.donasi', 'Program Donasi')
    keterangan = fields.Text('Keterangan')
    saldo = fields.Float('Saldo', compute='_compute_total_nilai_donasi')
    tersalurkan = fields.Float('Tersalurkan', compute='_compute_total_nilai_terima')
    date_begin = fields.Datetime(string='Start Date', required=True, tracking=True)
    date_end = fields.Datetime(string='End Date', required=True, tracking=True)
    yayasan_id = fields.Many2one('res.partner', 'Yayasan')
    person_id = fields.Many2one('res.users', 'Create Person')
    donatur_donasi_ids = fields.One2many('register.donasi.donatur', 'donasi_id', 'Donatur Donasi')
    penerima_donasi_ids = fields.One2many('register.penerima', 'donasi_id', 'Penerima Donasi')
    target_terkumpul = fields.Float('Target Terkumpul', compute='_compute_target_terkumpul_donasi')
    progres_saldo_terkumpul = fields.Float('Progres Saldo Terkumpul', compute='_compute_progres_saldo_terkumpul', store=True)
    jumlah_donatur = fields.Integer('Jumlah Donatur', compute='_compute_jumlah_donatur')
    jumlah_penerima = fields.Integer('Jumlah Penerima', compute='_compute_jumlah_penerima')
    total_rcn_donasi = fields.Float('Total Paket', compute='_compute_total_rab_donasi')
    rab_donasi_ids = fields.One2many('rab.donasi.line', 'donasi_management_id', string='RAB Donasi', )
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('publish', 'Publish'),
    ], string='State', readonly=True, default='draft', required=True, tracking=True)

    def func_approved(self):
        if self.state == 'draft':
            self.state = 'approved'

    def func_refused(self):
        if self.state == 'draft':
            self.state = 'refused'
    
    def func_publish(self):
        if self.state == 'approved':
            self.state = 'publish'

    @api.depends('total_rcn_donasi', 'target_terkumpul')
    def _compute_target_terkumpul_donasi(self):
        for donasi in self:
            donasi.target_terkumpul = donasi.total_rcn_donasi

    @api.depends('rab_donasi_ids.total_paket')
    def _compute_total_rab_donasi(self):
        for record in self:
            jumlah_rab_donasi = sum(total_rcn_donasi.total_paket for total_rcn_donasi in record.rab_donasi_ids)
            record.total_rcn_donasi = jumlah_rab_donasi

    @api.depends('donatur_donasi_ids')
    def _compute_jumlah_donatur(self):
        for record in self:
            record.jumlah_donatur = len(record.donatur_donasi_ids)

    @api.depends('penerima_donasi_ids')
    def _compute_jumlah_penerima(self):
        for record in self:
            record.jumlah_penerima = len(record.penerima_donasi_ids)

    @api.depends('saldo', 'target_terkumpul')
    def _compute_progres_saldo_terkumpul(self):
        for record in self:
            if record.target_terkumpul > 0:
                progress = (record.saldo / record.target_terkumpul) * 100
                record.progres_saldo_terkumpul = min(100, progress)
            else:
                record.progres_saldo_terkumpul = 0

    @api.depends('donatur_donasi_ids.nilai_donasi')
    def _compute_total_nilai_donasi(self):
        for donasi in self:
            total = sum(donasi.donatur_donasi_ids.mapped('nilai_donasi'))
            donasi.saldo = total
            # Jika total nilai donasi sama dengan saldo, Anda dapat mengubah status atau melakukan tindakan lain di sini jika diperlukan.

    @api.depends('penerima_donasi_ids.nilai_terima')
    def _compute_total_nilai_terima(self):
        for penerima in self:
            total = sum(penerima.penerima_donasi_ids.mapped('nilai_terima'))
            penerima.tersalurkan = total
            # Jika total nilai donasi sama dengan saldo, Anda dapat mengubah status atau melakukan tindakan lain di sini jika diperlukan.

class register_donasi_donatur(models.Model):
    _name = "register.donasi.donatur"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Register Donasi Donatur"
    _rec_name = 'code'

    donasi_id = fields.Many2one('donasi.management', string='Donasi', required=True)
    product_id = fields.Many2one('product.product', 'Produk')
    donatur_id = fields.Many2one('master.donatur', 'Donatur')
    email = fields.Char(string='Email', related='donatur_id.email')
    phone = fields.Char(string='Phone', related='donatur_id.phone')
    infaq_date = fields.Date('Tanggal Donasi')
    nilai_donasi = fields.Float('Nilai Donasi')
    total_donasi = fields.Float('Total Donasi', compute='_compute_total_nilai_donasi')
    note = fields.Char('Note', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    code = fields.Char(string="Number", readonly=True, required=True, copy=False, default='New')
    qty = fields.Integer('Qty')

    @api.depends('nilai_donasi', 'qty')
    def _compute_total_nilai_donasi(self):
        for jumlah_donasi in self:
            total = jumlah_donasi.qty * jumlah_donasi.nilai_donasi
            jumlah_donasi.total_donasi = total

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = self.env["ir.sequence"].next_by_code("register.dontur.sequence") or 'New'
        result = super(register_donasi_donatur, self).create(vals)
        return result

    @api.onchange('donatur_id')
    def _onchange_donatur_id(self):
        if self.donatur_id:
            self.partner_id = self.donatur_id.partner_id

    @api.model_create_single
    def create(self, values):
        if 'donatur_id' in values:
            donatur = self.env['master.donatur'].browse(values['donatur_id'])
            values['partner_id'] = donatur.partner_id.id
        self.create_sale_order(values)
        return super(register_donasi_donatur, self).create(values)

    def create_sale_order(self, values):
        if 'product_id' in values:
            sale_order_obj = self.env['sale.order']
            sale_order_line_obj = self.env['sale.order.line']

            vals = {
                'partner_id': values['partner_id'],
                'date_order': values['infaq_date'],
                'donasi_id': values['donasi_id'],
            }
            sale_order = sale_order_obj.create(vals)
            sale_order.donasi_id = values['donasi_id']

            so_line_vals = {
                'product_id': values['product_id'],
                'name': values['note'],
                'price_unit': values['nilai_donasi'],
                'product_uom_qty': 1,
                'order_id': sale_order.id,
            }
            sale_order_line = sale_order_line_obj.create(so_line_vals)

            # Membuat faktur pelanggan
            sale_order.action_confirm()  # Konfirmasi pesanan penjualan
            invoice = sale_order._create_invoices()

            if invoice:
                invoice.write({'state': 'draft'})
                
        return True

class register_penerima(models.Model):
    _name = "register.penerima"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Register Penerima"
    _rec_name = 'donasi_id'

    donasi_id = fields.Many2one('donasi.management', string='Donasi', required=True)
    product_id = fields.Many2one('product.product', 'Produk')
    penerima_id = fields.Many2one('master.penerima', 'Penerima')
    date = fields.Date('Tanggal Terima')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone', related='penerima_id.phone')
    tipe_penerima = fields.Many2one('master.tipe.penerima', 'Tipe Penerima')
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    nilai_terima = fields.Float('Nilai Terima')
    note = fields.Char('Note')

    @api.onchange('penerima_id')
    def _onchange_penerima_id(self):
        if self.penerima_id:
            self.partner_id = self.penerima_id.partner_id

    @api.model_create_single
    def create(self, values):
        if 'penerima_id' in values:
            penerima = self.env['master.penerima'].browse(values['penerima_id'])
            values['partner_id'] = penerima.partner_id.id

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
        return super(register_penerima, self).create(values)

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
            'donasi_id': values['donasi_id'],
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
                'partner_id': values['partner_id'],
                'date_order': values['date'],
                'donasi_id': values['donasi_id'],
            }
            purchase_order = purchase_order_obj.create(vals)
            purchase_order.donasi_id = values['donasi_id']

            po_line_vals = {
                'product_id': values['product_id'],
                'name': values['note'],
                'price_unit': values['nilai_terima'],
                'product_qty': 1,
                'order_id': purchase_order.id,
            }
            purchase_order_line = purchase_order_line_obj.create(po_line_vals)

            # Membuat faktur pelanggan
            purchase_order.button_confirm()
            purchase_order.action_create_invoice()

            # Cari faktur pelanggan yang dibuat dari purchase order
            vendorbill = account_move_obj.search([('purchase_id', '=', purchase_order.id)])

            if vendorbill:
                vendorbill.write({'donasi_id': values['donasi_id']})

        return True



    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.deskripsi = self.product_id.name
    #         self.nilai_wakaf = self.product_id.lst_price

class rab_donasi_line(models.Model):
    _name = "rab.donasi.line"
    _description = "RAB Donasi Line"

    donasi_management_id = fields.Many2one('donasi.management', 'Donasi Management')
    product_id = fields.Many2one('product.product', 'Produk')
    qty = fields.Integer('Qty', default=1)
    uom_id = fields.Many2one('uom.uom', 'Uom')
    deskripsi = fields.Char('Deskripsi')
    nilai_paket = fields.Float('Nilai Paket')
    total_paket = fields.Float('Total Pakte', compute='_compute_total_nilai_paket')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            # Isi uom_id dengan uom dari product_id
            self.uom_id = self.product_id.uom_id.id

    @api.depends('nilai_paket', 'qty')
    def _compute_total_nilai_paket(self):
        for jumlah in self:
            penjumlahan = jumlah.qty * jumlah.nilai_paket
            jumlah.total_paket = penjumlahan

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.nilai_paket = self.product_id.list_price