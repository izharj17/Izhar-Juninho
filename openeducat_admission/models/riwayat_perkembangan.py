from odoo import models, fields, api, _

class TumbuhKembang(models.Model):
    _name = "tumbuh.kembang"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Formulir Tumbuh Kembang"
    _rec_name = 'nama_anak'
    _order = 'id DESC'

    #identitas anak
    nama_anak = fields.Char('Nama Lengkap')
    nama_panggilan = fields.Char('Nama Panggilan')
    tempat_lahir = fields.Char('Tempat Lahir')
    tgl_lahir = fields.Date('Tanggal Lahir')
    suku = fields.Char('Suku Bangsa')
    agama = fields.Char('Agama')
    alamat = fields.Text('Alamat')
    urutan = fields.Integer('Urutan dalam keluarga anak ke')
    
    #susunan dalam keluarga
    susunan = fields.Text('Susunan Anak Dalam Keluarga')
    
    #data ayah
    nama_ayah = fields.Char('Nama Lengkap Ayah')
    tempat_lahir_ayah = fields.Char('Tempat Lahir Ayah')
    tgl_lahir_ayah = fields.Date('Tanggal Lahir')
    suku_ayah = fields.Char('Suku Bangsa Ayah')
    agama_ayah = fields.Char('Agama Ayah')
    pendidikan_ayah = fields.Char('Pendidikan Terakhir Ayah')
    pekerjaan_ayah = fields.Char('Pekerjaan Ayah')
    usia_menikah_ayah = fields.Char('Usia Ayah Saat Menikah')
    alamat_ayah = fields.Char('Alamat Ayah')
    telp_ayah = fields.Integer('Telp/Hp Ayah')
    
    #data ibu
    nama_ibu = fields.Char('Nama Lengkap Ibu')
    tempat_lahir_ibu = fields.Char('Tempat Lahir Ibu')
    tgl_lahir_ibu = fields.Date('Tanggal Lahir Ibu')
    suku_ibu = fields.Char('Suku Bangsa Ibu')
    agama_ibu = fields.Char('Agama Ibu')
    pendidikan_ibu = fields.Char('Pendidikan Terakhir Ibu')
    pekerjaan_ibu = fields.Char('Pekerjaan Ibu')
    usia_menikah_ibu = fields.Char('Usia Ibu Saat Menikah')
    alamat_ibu = fields.Char('Alamat Ibu')
    telp_ibu = fields.Integer('Telp/Hp Ibu')
    
    #data wali
    nama_wali = fields.Char('Nama Lengkap Wali')
    tempat_lahir_wali = fields.Char('Tempat Lahir Wali')
    tgl_lahir_wali = fields.Date('Tanggal Lahir Wali')
    suku_wali = fields.Char('Suku Bangsa Wali')
    agama_wali = fields.Char('Agama Wali')
    pendidikan_wali = fields.Char('Pendidikan Terakhir Wali')
    pekerjaan_wali = fields.Char('Pekerjaan Wali')
    alamat_wali = fields.Char('Alamat Wali')
    telp_wali = fields.Integer('Telp/Hp Wali')
    
    #masa pranatal
    usia_mengandung = fields.Char('Usia Saat Ibu Mengandung (Tahun)')
    kondisi_ibu = fields.Text('Kondisi Ibu Saat Mengandung')
    kondisi_bayi = fields.Text('Kondisi Bayi dalam Kandungan')
    
    #masa pratus
    usia_kandungan = fields.Char('Usia Kandungan Saat Lahir')
    proses_kelahiran = fields.Text('Proses Kelahiran')
    kondisi_lahir = fields.Text('Tempat Lahir, Waktu, Proporsi dan Kondisi Saat Lahir')
    
    #masa posnatal
    pertumbuhan = fields.Char('Pertumbuhan Tubuh / Fisik Setelah Lahir')
    motorik_kasar = fields.Char('Perkembangan Motorik Kasar (merangkak, duduk, berjalan, berlari dsb)')
    motorik_halus = fields.Char('Perkembangan MotoriK Halus (memegang, menggenggam, menggunakan alat seperti pensil, menggambar, menulis, mencoret, dsb)')
    bahasa = fields.Char('Perkembangan Bahasa Secara Umum')
    berbicara = fields.Char('Aktivitas Berbicara')
    kognitif = fields.Char('Kemampuan Kognitif Secara Umum ( menangkap, memahami intruksi / informasi baru )')
    konsentrasi = fields.Char('Konsentrasi')
    atensi = fields.Char('Rentang Atensi / Perhatian')
    adaptasi = fields.Char('Kemampuan Adaptasi Sosial')
    aktivitas = fields.Char('Level Aktivitas (proporsi aktif tidaknya anak)')
    keterarahan = fields.Char('Keterarahan Aktivitas (Bertujuan / menikmati / asyik beraktifitas tertentu)')
    interaksi = fields.Char('Interaksi Anak Dengan Keluarga / Lingkungan Rumah (dekat / akur / sering konflik, dsb)')
    kebiasaan = fields.Char('Kebiasaan Anak Dilingkungan Rumah')
    keluhan = fields.Char('Keluhan / Kesulitan yang Serimg Diungkapkan Anak')
    perilaku = fields.Char('Perilaku “Sulit / Bermasalah“ yang sering diperlihatkan anak')
    kesulitan = fields.Char('Keluhan / kesulitan orang tua dalam mengasuh / mendidik anak yang bersangkutan')
    penyakit = fields.Char('Penyakit / kelainan / kecelakaan berat yang pernah dialami anak ( yang memerlukan perawatan lama di rumah / RS ) serta jenis terapi yang pernah / sedang dijalani anak')
    makanan = fields.Char('Makanan yang tidak boleh dikonsumsi :')
    alergi = fields.Char('Alergi')
    keterangan_lain = fields.Char('Data / keterangan lain yang dianggap perlu untuk ditambahkan & diketahui pihak lain')