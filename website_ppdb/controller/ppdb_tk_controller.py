from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
import json
import base64
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class WebsitePPDBTK(http.Controller):

    @http.route('/api/admission_tk', type='http', auth='public', methods=['POST'], csrf=False,  website=True)
    def create_admission_tk(self, **post):
        try:
            # Ambil data dari request
           # register_id = post.get('register_id')
            register_id = 3
            name = post.get('nama_lengkap')
            if name:
                name_parts = name.split()
                if len(name_parts) == 2:
                    first_name, last_name = name_parts[0], name_parts[1]
                    middle_name = ""
                elif len(name_parts) >= 3:
                    first_name = name_parts[0]
                    last_name = name_parts[-1]
                    middle_name = " ".join(name_parts[1:-1])
                else:
                    first_name = name_parts[0]
                    middle_name = ""
                    last_name = ""
            else:
                first_name = ""
                middle_name = ""
                last_name = ""
            # first_name = post.get('first_name')
            # middle_name = post.get('middle_name')
            # last_name = post.get('last_name')
            gender = post.get('gender')
            birth_place = post.get('birth_place')
            birth_date = post.get('birth_date')
            alamat_siswa = post.get('alamat_siswa')
            email = post.get('email')
            # nama_panggilan = post.get('nama_panggilan')
            # Data tambahan
            # nisn = post.get('nisn')
            # nik = post.get('nik')
            # no_kk = post.get('no_kk')
            # no_akta_lahir = post.get('no_akta_lahir')
            agama = post.get('agama')
            # kewarganegaraan = post.get('kewarganegaraan')
            # rt_rw = post.get('rt_rw')
            # kecamatan_id = post.get('kecamatan_id')
            # kelurahan_id = post.get('kelurahan_id')
            # kode_pos = post.get('kode_pos')
            # tempat_tinggal = post.get('tempat_tinggal')
            # moda_transport = post.get('moda_transport')
            anak_ke = post.get('anak_ke')
            # punya_kia = post.get('punya_kia')
            jenis_ppdb = post.get('jenis_ppdb')
            asal_sekolah = post.get('asal_sekolah')
            alamat_sekolah = post.get('alamat_sekolah')
            
            # Data ayah
            ayah_id = post.get('ayah_id')
            tempat_lahir_ayah = post.get('tempat_lahir_ayah')
            tgl_lahir_ayah = post.get('tgl_lahir_ayah')
            telp_ayah = post.get('telp_ayah')
            email_ayah = post.get('email_ayah')
            # suku_ayah = post.get('suku_ayah')
            agama_ayah = post.get('agama_ayah')
            pendidikan_ayah = post.get('pendidikan_ayah')
            pekerjaan_ayah = post.get('pekerjaan_ayah')
            jabatan_ayah = post.get('jabatan_ayah')
            penghasilan_ayah = post.get('penghasilan_ayah')
            tanggungan_ayah = post.get('tanggungan_ayah')
            status_ayah = post.get('status_ayah')
            alamat_ayah = post.get('alamat_ayah')
            
            # Data ibu
            ibu_id = post.get('ibu_id')
            tempat_lahir_ibu = post.get('tempat_lahir_ibu')
            tgl_lahir_ibu = post.get('tgl_lahir_ibu')
            telp_ibu = post.get('telp_ibu')
            email_ibu = post.get('email_ibu')
            suku_ibu = post.get('suku_ibu')
            agama_ibu = post.get('agama_ibu')
            pendidikan_ibu = post.get('pendidikan_ibu')
            pekerjaan_ibu = post.get('pekerjaan_ibu')
            jabatan_ibu = post.get('jabatan_ibu')
            penghasilan_ibu = post.get('penghasilan_ibu')
            tanggungan_ibu = post.get('tanggungan_ibu')
            status_ibu = post.get('status_ibu')
            alamat_ibu = post.get('alamat_ibu')


            # Fetch or create Ayah record based on name
            ayah_name = post.get('ayah_name')
            ayah_id = request.env['op.data.ayah'].sudo().search([('name_ayah', '=', ayah_name)], limit=1)
            if not ayah_id:
                ayah_id = request.env['op.data.ayah'].sudo().create({
                    'name_ayah': ayah_name,
                    # Additional fields for Ayah can be set here if provided in post
                    'thn_lahir': post.get('tgl_lahir_ayah')or None,
                    'agama': post.get('agama_ayah'),
                    'pendidikan': post.get('pendidikan_ayah'),
                    'pekerjaan': post.get('pekerjaan_ayah'),
                    'alamat': post.get('alamat_ayah'),
                    'email': post.get('email_ayah'),
                    'no_wa': post.get('telp_ayah'),
                    # Add other fields as necessary
                }).id
            else:
                ayah_id = ayah_id.id

            # Fetch or create Ibu record based on name
            ibu_name = post.get('ibu_name')
            ibu_id = request.env['op.data.ibu'].sudo().search([('name_ibu', '=', ibu_name)], limit=1)
            if not ibu_id:
                ibu_id = request.env['op.data.ibu'].sudo().create({
                    'name_ibu': ibu_name,
                    # Additional fields for Ibu can be set here if provided in post
                    'thn_lahir': post.get('tgl_lahir_ibu')or None,
                    'agama': post.get('agama_ibu'),
                    'pendidikan': post.get('pendidikan_ibu'),
                    'pekerjaan': post.get('pekerjaan_ibu'),
                    'alamat': post.get('alamat_ibu'),
                    'email': post.get('email_ibu'),
                    'no_wa': post.get('telp_ibu'),
                    # Add other fields as necessary
                }).id
            else:
                ibu_id = ibu_id.id


            # Data tambahan lainnya
            # tinggi_bdn = post.get('tinggi_bdn')
            # berat_bdn = post.get('berat_bdn')
            # lingkar_kpl = post.get('lingkar_kpl')
            # jrk_tmpt_plhn = post.get('jrk_tmpt_plhn')
            # jrk_tmpt_km = post.get('jrk_tmpt_km')
            # waktu_tempuh = post.get('waktu_tempuh')
            # jmlh_saudara_kandung = post.get('jmlh_saudara_kandung')

            #Kandungan
            usia_kandungan = post.get('usia_kandungan')
            proses_lahir = post.get('proses_lahir')


            # Data Makan & Minum
            asi = post.get('asi')
            lama_asi = post.get('lama_asi')
            susu = post.get('susu')
            anak_minum = post.get('anak_minum')
            makan_padat = post.get('makan_padat')
            favorit = post.get('favorit')
            ga_favorit = post.get('ga_favorit')
            makan_sendiri = post.get('makan_sendiri')
            alergi = post.get('alergi')

            # Data Tidur
            tidur = post.get('tidur')
            kamar = post.get('kamar')
            tempat_tidur = post.get('tempat_tidur')
            teman_tidur = post.get('teman_tidur')
            jam_tidur = post.get('jam_tidur')
            bangun_malam = post.get('bangun_malam')
            jam_bangun = post.get('jam_bangun')
            tidur_siang = post.get('tidur_siang')
            mengantuk = post.get('mengantuk')
            kebiasaan_tidur = post.get('kebiasaan_tidur')

            # Toilet Training Fields
            toilet = post.get('toilet')
            berhasil_toilet = post.get('berhasil_toilet')
            mulai_toilet = post.get('mulai_toilet')
            ngompol = post.get('ngompol')
            tidak_ngompol = post.get('tidak_ngompol')
            kencing_malam = post.get('kencing_malam')
            bantuan_toilet = post.get('bantuan_toilet')

            # Additional fields for 'Bermain' section
            bermain = post.get('bermain')
            teman_main = post.get('teman_main')
            orang_rumah = post.get('orang_rumah')
            ket_bermain = post.get('ket_bermain')
            hubungan_dekat = post.get('hubungan_dekat')
            kegiatan_anak = post.get('kegiatan_anak')

            # Fields for 'Hobi dan Pertemanan'
            # hobi_anak = post.get('hobi_anak')
            # teman_hobi = post.get('teman_hobi')
            # kecenderungan = post.get('kecenderungan')
            # teman_sebaya = post.get('teman_sebaya')
            # hal_disukai = post.get('hal_disukai')

            # Fields for 'Pembelajaran'
            atmosfer_singkat = post.get('atmosfer_singkat')
            sekolah_dicari = post.get('sekolah_dicari')
            deskripsi = post.get('deskripsi')
            proses_belajar = post.get('proses_belajar')
            metode_disiplin = post.get('metode_disiplin')
            metode_aturan = post.get('metode_aturan')
            metode_pendekatan = post.get('metode_pendekatan')

            # Fields for 'Temperament'
            agresif = post.get('agresif')
            aktif = post.get('aktif')
            berani = post.get('berani')
            cengeng = post.get('cengeng')
            cerewet = post.get('cerewet')
            ceria = post.get('ceria')
            dominan = post.get('dominan')
            pengikut = post.get('pengikut')
            humoris = post.get('humoris')
            ingin_tahu = post.get('ingin_tahu')
            keras_kepala = post.get('keras_kepala')
            kreatif = post.get('kreatif')
            mudah_akrab = post.get('mudah_akrab')
            mudah_bergaul = post.get('mudah_bergaul')
            berjiwa_pengasuh = post.get('berjiwa_pengasuh')
            pandai = post.get('pandai')
            patuh = post.get('patuh')
            pemaaf = post.get('pemaaf')
            penakut = post.get('penakut')
            pemalu = post.get('pemalu')
            pemarah = post.get('pemarah')
            pembangkang = post.get('pembangkang')
            pemberi = post.get('pemberi')
            pembohong = post.get('pembohong')
            pemurung = post.get('pemurung')
            pemimpin = post.get('pemimpin')
            pemelas = post.get('pemelas')
            pendiam = post.get('pendiam')
            penghayal = post.get('penghayal')
            penuh_perhatian = post.get('penuh_perhatian')
            penyayang = post.get('penyayang')
            penyendiri = post.get('penyendiri')
            rajin = post.get('rajin')
            sabar = post.get('sabar')
            senang_berteman = post.get('senang_berteman')
            sensitif = post.get('sensitif')
            lainnya = post.get('lainnya')

            # TTD fields
            hari_pengisian = post.get('hari_pengisian')
            tanggal_pengisian = post.get('tanggal_pengisian')
            ttd_ayah = post.get('ttd_ayah')
            ttd_ibu = post.get('ttd_ibu')

            file_akta = request.httprequest.files.get('file_akta')
            file_pas_ft = request.httprequest.files.get('file_pas_ft')
            file_kk = request.httprequest.files.get('file_kk')
            file_ktp_ortu = request.httprequest.files.get('file_ktp_ortu')

            file_akta_base64 = base64.b64encode(file_akta.read()) if file_akta else None
            file_pas_ft_base64 = base64.b64encode(file_pas_ft.read()) if file_pas_ft else None
            file_kk_base64 = base64.b64encode(file_kk.read()) if file_kk else None
            file_ktp_ortu_base64 = base64.b64encode(file_ktp_ortu.read()) if file_ktp_ortu else None


            # Buat record baru di model formulir.sm
            admission = request.env['formulir.tk'].sudo().create({
                'register_id': register_id,
                'name': name,
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                # 'nama_panggilan':nama_panggilan,
                'gender': gender,
                'birth_place': birth_place,
                'birth_date': birth_date,
                'alamat_siswa': alamat_siswa,
                'email': email,
                # 'nisn': nisn,
                # 'nik': nik,
                # 'no_kk': no_kk,
                # 'no_akta_lahir': no_akta_lahir,
                'agama': agama,
                # 'kewarganegaraan': kewarganegaraan,
                # 'rt_rw': rt_rw,
                # 'kecamatan_id': kecamatan_id,
                # 'kelurahan_id': kelurahan_id,
                # 'kode_pos': kode_pos,
                # 'tempat_tinggal': tempat_tinggal,
                # 'moda_transport': moda_transport,
                'anak_ke': anak_ke,
                # 'punya_kia': punya_kia,
                # 'jenis_ppdb': jenis_ppdb,
                'asal_sekolah': asal_sekolah,
                # 'alamat_sekolah': alamat_sekolah,
                'ayah_id': ayah_id,
                'tempat_lahir_ayah': tempat_lahir_ayah,
                'tgl_lahir_ayah': tgl_lahir_ayah,
                'telp_ayah': telp_ayah,
                'email_ayah': email_ayah,
                # 'suku_ayah': suku_ayah,
                'agama_ayah': agama_ayah,
                'pendidikan_ayah': pendidikan_ayah,
                'pekerjaan_ayah': pekerjaan_ayah,
                'jabatan_ayah': jabatan_ayah,
                'penghasilan_ayah': penghasilan_ayah,
                'tanggungan_ayah': tanggungan_ayah,
                'status_ayah': status_ayah,
                'alamat_ayah': alamat_ayah,
                'ibu_id': ibu_id,
                'tempat_lahir_ibu': tempat_lahir_ibu,
                'tgl_lahir_ibu': tgl_lahir_ibu,
                'telp_ibu': telp_ibu,
                'email_ibu': email_ibu,
                'suku_ibu': suku_ibu,
                'agama_ibu': agama_ibu,
                'pendidikan_ibu': pendidikan_ibu,
                'pekerjaan_ibu': pekerjaan_ibu,
                'jabatan_ibu': jabatan_ibu,
                'penghasilan_ibu': penghasilan_ibu,
                'tanggungan_ibu': tanggungan_ibu,
                'status_ibu': status_ibu,
                'alamat_ibu': alamat_ibu,
                # 'tinggi_bdn': tinggi_bdn,
                # 'berat_bdn': berat_bdn,
                # 'lingkar_kpl': lingkar_kpl,
                # 'jrk_tmpt_plhn': jrk_tmpt_plhn,
                # 'jrk_tmpt_km': jrk_tmpt_km,
                # 'waktu_tempuh': waktu_tempuh,
                # 'jmlh_saudara_kandung': jmlh_saudara_kandung,
                'usia_kandungan' : usia_kandungan,
                'proses_lahir' : proses_lahir,
                'asi': asi,
                'lama_asi': lama_asi,
                'susu': susu,
                'anak_minum': anak_minum,
                'makan_padat': makan_padat,
                'favorit': favorit,
                'ga_favorit': ga_favorit,
                'makan_sendiri': makan_sendiri,
                'alergi': alergi,
                'tidur': tidur,
                'kamar': kamar,
                'tempat_tidur': tempat_tidur,
                'teman_tidur': teman_tidur,
                'jam_tidur': jam_tidur,
                'bangun_malam': bangun_malam,
                'jam_bangun': jam_bangun,
                'tidur_siang': tidur_siang,
                'mengantuk': mengantuk,
                'kebiasaan_tidur': kebiasaan_tidur,

                # Toilet Training Fields
                'toilet': toilet,
                'berhasil_toilet': berhasil_toilet,
                'mulai_toilet': mulai_toilet,
                'ngompol': ngompol,
                'tidak_ngompol': tidak_ngompol,
                'kencing_malam': kencing_malam,
                'bantuan_toilet': bantuan_toilet,

                # Additional fields for 'Bermain' section
                'bermain': bermain,
                'teman_main': teman_main,
                'orang_rumah': orang_rumah,
                'ket_bermain': ket_bermain,
                'hubungan_dekat': hubungan_dekat,
                'kegiatan_anak': kegiatan_anak,

                # Fields for 'Hobi dan Pertemanan'
                # 'hobi_anak': hobi_anak,
                # 'teman_hobi': teman_hobi,
                # 'kecenderungan': kecenderungan,
                # 'teman_sebaya': teman_sebaya,
                # 'hal_disukai': hal_disukai,

                # Fields for 'Pembelajaran'
                'atmosfer_singkat': atmosfer_singkat,
                'sekolah_dicari': sekolah_dicari,
                'deskripsi': deskripsi,
                'proses_belajar': proses_belajar,
                'metode_disiplin': metode_disiplin,
                'metode_aturan': metode_aturan,
                'metode_pendekatan': metode_pendekatan,

                # Fields for 'Temperament'
                'agresif': agresif,
                'aktif': aktif,
                'berani': berani,
                'cengeng': cengeng,
                'cerewet': cerewet,
                'ceria': ceria,
                'dominan': dominan,
                'pengikut': pengikut,
                'humoris': humoris,
                'ingin_tahu': ingin_tahu,
                'keras_kepala': keras_kepala,
                'kreatif': kreatif,
                'mudah_akrab': mudah_akrab,
                'mudah_bergaul': mudah_bergaul,
                'berjiwa_pengasuh': berjiwa_pengasuh,
                'pandai': pandai,
                'patuh': patuh,
                'pemaaf': pemaaf,
                'penakut': penakut,
                'pemalu': pemalu,
                'pemarah': pemarah,
                'pembangkang': pembangkang,
                'pemberi': pemberi,
                'pembohong': pembohong,
                'pemurung': pemurung,
                'pemimpin': pemimpin,
                'pemelas': pemelas,
                'pendiam': pendiam,
                'penghayal': penghayal,
                'penuh_perhatian': penuh_perhatian,
                'penyayang': penyayang,
                'penyendiri': penyendiri,
                'rajin': rajin,
                'sabar': sabar,
                'senang_berteman': senang_berteman,
                'sensitif': sensitif,
                'lainnya': lainnya,

                # TTD fields
                'hari_pengisian': hari_pengisian,
                'tanggal_pengisian': tanggal_pengisian,
                'ttd_ayah': ttd_ayah,
                'ttd_ibu': ttd_ibu,
            })
            
            return Response(json.dumps({
                'status': 200,
                'message': 'Admission created successfully',
                'admission_id': admission.id,
                # 'lama_asi':lama_asi
            }), content_type='application/json', status=200)
        except Exception as e:
            return Response(json.dumps({
                'status': 500,
                'message': str(e)
            }), content_type='application/json', status=500)


    # @http.route('/api/admission_tk', type='json', auth='public', methods=['POST'], csrf=False)
    # def create_admission_tk(self, **kwargs):
    #     try:
    #         # Ambil data dari request
    #        # register_id = post.get('register_id')
    #         register_id = 3
    #         name = post.get('nama_lengkap')
    #         if name:
    #             name_parts = name.split()
    #             if len(name_parts) == 2:
    #                 first_name, last_name = name_parts[0], name_parts[1]
    #                 middle_name = ""
    #             elif len(name_parts) >= 3:
    #                 first_name = name_parts[0]
    #                 last_name = name_parts[-1]
    #                 middle_name = " ".join(name_parts[1:-1])
    #             else:
    #                 first_name = name_parts[0]
    #                 middle_name = ""
    #                 last_name = ""
    #         else:
    #             first_name = ""
    #             middle_name = ""
    #             last_name = ""
    #         # first_name = post.get('first_name')
    #         # middle_name = post.get('middle_name')
    #         # last_name = post.get('last_name')
    #         gender = kwargs.get('gender')
    #         birth_place = kwargs.get('birth_place')
    #         birth_date = kwargs.get('birth_date')
    #         alamat_siswa = kwargs.get('alamat_siswa')
    #         email = kwargs.get('email')
    #         # nama_panggilan = post.get('nama_panggilan')
    #         # Data tambahan
    #         # nisn = kwargs.get('nisn')
    #         # nik = kwargs.get('nik')
    #         # no_kk = kwargs.get('no_kk')
    #         # no_akta_lahir = kwargs.get('no_akta_lahir')
    #         agama = kwargs.get('agama')
    #         # kewarganegaraan = kwargs.get('kewarganegaraan')
    #         # rt_rw = kwargs.get('rt_rw')
    #         # kecamatan_id = kwargs.get('kecamatan_id')
    #         # kelurahan_id = kwargs.get('kelurahan_id')
    #         # kode_pos = kwargs.get('kode_pos')
    #         # tempat_tinggal = kwargs.get('tempat_tinggal')
    #         # moda_transport = kwargs.get('moda_transport')
    #         anak_ke = kwargs.get('anak_ke')
    #         # punya_kia = kwargs.get('punya_kia')
    #         jenis_ppdb = kwargs.get('jenis_ppdb')
    #         asal_sekolah = kwargs.get('asal_sekolah')
    #         alamat_sekolah = kwargs.get('alamat_sekolah')
            
    #         # Data ayah
    #         ayah_id = kwargs.get('ayah_id')
    #         tempat_lahir_ayah = kwargs.get('tempat_lahir_ayah')
    #         tgl_lahir_ayah = kwargs.get('tgl_lahir_ayah')
    #         telp_ayah = kwargs.get('telp_ayah')
    #         email_ayah = kwargs.get('email_ayah')
    #         # suku_ayah = kwargs.get('suku_ayah')
    #         agama_ayah = kwargs.get('agama_ayah')
    #         pendidikan_ayah = kwargs.get('pendidikan_ayah')
    #         pekerjaan_ayah = kwargs.get('pekerjaan_ayah')
    #         jabatan_ayah = kwargs.get('jabatan_ayah')
    #         penghasilan_ayah = kwargs.get('penghasilan_ayah')
    #         tanggungan_ayah = kwargs.get('tanggungan_ayah')
    #         status_ayah = kwargs.get('status_ayah')
    #         alamat_ayah = kwargs.get('alamat_ayah')
            
    #         # Data ibu
    #         ibu_id = kwargs.get('ibu_id')
    #         tempat_lahir_ibu = kwargs.get('tempat_lahir_ibu')
    #         tgl_lahir_ibu = kwargs.get('tgl_lahir_ibu')
    #         telp_ibu = kwargs.get('telp_ibu')
    #         email_ibu = kwargs.get('email_ibu')
    #         suku_ibu = kwargs.get('suku_ibu')
    #         agama_ibu = kwargs.get('agama_ibu')
    #         pendidikan_ibu = kwargs.get('pendidikan_ibu')
    #         pekerjaan_ibu = kwargs.get('pekerjaan_ibu')
    #         jabatan_ibu = kwargs.get('jabatan_ibu')
    #         penghasilan_ibu = kwargs.get('penghasilan_ibu')
    #         tanggungan_ibu = kwargs.get('tanggungan_ibu')
    #         status_ibu = kwargs.get('status_ibu')
    #         alamat_ibu = kwargs.get('alamat_ibu')


    #         # Fetch or create Ayah record based on name
    #         ayah_name = post.get('ayah_name')
    #         ayah_id = request.env['op.data.ayah'].sudo().search([('name_ayah', '=', ayah_name)], limit=1)
    #         if not ayah_id:
    #             ayah_id = request.env['op.data.ayah'].sudo().create({
    #                 'name_ayah': ayah_name,
    #                 # Additional fields for Ayah can be set here if provided in kwargs
    #                 'thn_lahir': post.get('tgl_lahir_ayah')or None,
    #                 'agama': post.get('agama_ayah'),
    #                 'pendidikan': post.get('pendidikan_ayah'),
    #                 'pekerjaan': post.get('pekerjaan_ayah'),
    #                 'alamat': post.get('alamat_ayah'),
    #                 'email': post.get('email_ayah'),
    #                 'no_wa': post.get('telp_ayah'),
    #                 # Add other fields as necessary
    #             }).id
    #         else:
    #             ayah_id = ayah_id.id

    #         # Fetch or create Ibu record based on name
    #         ibu_name = post.get('ibu_name')
    #         ibu_id = request.env['op.data.ibu'].sudo().search([('name_ibu', '=', ibu_name)], limit=1)
    #         if not ibu_id:
    #             ibu_id = request.env['op.data.ibu'].sudo().create({
    #                 'name_ibu': ibu_name,
    #                 # Additional fields for Ibu can be set here if provided in kwargs
    #                 'thn_lahir': post.get('tgl_lahir_ibu')or None,
    #                 'agama': post.get('agama_ibu'),
    #                 'pendidikan': post.get('pendidikan_ibu'),
    #                 'pekerjaan': post.get('pekerjaan_ibu'),
    #                 'alamat': post.get('alamat_ibu'),
    #                 'email': post.get('email_ibu'),
    #                 'no_wa': post.get('telp_ibu'),
    #                 # Add other fields as necessary
    #             }).id
    #         else:
    #             ibu_id = ibu_id.id


    #         # Data tambahan lainnya
    #         # tinggi_bdn = kwargs.get('tinggi_bdn')
    #         # berat_bdn = kwargs.get('berat_bdn')
    #         # lingkar_kpl = kwargs.get('lingkar_kpl')
    #         # jrk_tmpt_plhn = kwargs.get('jrk_tmpt_plhn')
    #         # jrk_tmpt_km = kwargs.get('jrk_tmpt_km')
    #         # waktu_tempuh = kwargs.get('waktu_tempuh')
    #         # jmlh_saudara_kandung = kwargs.get('jmlh_saudara_kandung')

    #         #Kandungan
    #         usia_kandungan = kwargs.get('usia_kandungan')
    #         proses_lahir = kwags.get('proses_lahir')


    #         # Data Makan & Minum
    #         asi = kwargs.get('asi')
    #         lama_asi = kwargs.get('lama_asi')
    #         susu = kwargs.get('susu')
    #         anak_minum = kwargs.get('anak_minum')
    #         makan_padat = kwargs.get('makan_padat')
    #         favorit = kwargs.get('favorit')
    #         ga_favorit = kwargs.get('ga_favorit')
    #         makan_sendiri = kwargs.get('makan_sendiri')
    #         alergi = kwargs.get('alergi')

    #         # Data Tidur
    #         tidur = kwargs.get('tidur')
    #         kamar = kwargs.get('kamar')
    #         tempat_tidur = kwargs.get('tempat_tidur')
    #         teman_tidur = kwargs.get('teman_tidur')
    #         jam_tidur = kwargs.get('jam_tidur')
    #         bangun_malam = kwargs.get('bangun_malam')
    #         jam_bangun = kwargs.get('jam_bangun')
    #         tidur_siang = kwargs.get('tidur_siang')
    #         mengantuk = kwargs.get('mengantuk')
    #         kebiasaan_tidur = kwargs.get('kebiasaan_tidur')

    #         # Toilet Training Fields
    #         toilet = kwargs.get('toilet')
    #         berhasil_toilet = kwargs.get('berhasil_toilet')
    #         mulai_toilet = kwargs.get('mulai_toilet')
    #         ngompol = kwargs.get('ngompol')
    #         tidak_ngompol = kwargs.get('tidak_ngompol')
    #         kencing_malam = kwargs.get('kencing_malam')
    #         bantuan_toilet = kwargs.get('bantuan_toilet')

    #         # Additional fields for 'Bermain' section
    #         bermain = kwargs.get('bermain')
    #         teman_main = kwargs.get('teman_main')
    #         orang_rumah = kwargs.get('orang_rumah')
    #         ket_bermain = kwargs.get('ket_bermain')
    #         hubungan_dekat = kwargs.get('hubungan_dekat')
    #         kegiatan_anak = kwargs.get('kegiatan_anak')

    #         # Fields for 'Hobi dan Pertemanan'
    #         hobi_anak = kwargs.get('hobi_anak')
    #         teman_hobi = kwargs.get('teman_hobi')
    #         kecenderungan = kwargs.get('kecenderungan')
    #         teman_sebaya = kwargs.get('teman_sebaya')
    #         hal_disukai = kwargs.get('hal_disukai')

    #         # Fields for 'Pembelajaran'
    #         atmosfer_singkat = kwargs.get('atmosfer_singkat')
    #         sekolah_dicari = kwargs.get('sekolah_dicari')
    #         deskripsi = kwargs.get('deskripsi')
    #         proses_belajar = kwargs.get('proses_belajar')
    #         metode_disiplin = kwargs.get('metode_disiplin')
    #         metode_aturan = kwargs.get('metode_aturan')
    #         metode_pendekatan = kwargs.get('metode_pendekatan')

    #         # Fields for 'Temperament'
    #         agresif = kwargs.get('agresif')
    #         aktif = kwargs.get('aktif')
    #         berani = kwargs.get('berani')
    #         cengeng = kwargs.get('cengeng')
    #         cerewet = kwargs.get('cerewet')
    #         ceria = kwargs.get('ceria')
    #         dominan = kwargs.get('dominan')
    #         pengikut = kwargs.get('pengikut')
    #         humoris = kwargs.get('humoris')
    #         ingin_tahu = kwargs.get('ingin_tahu')
    #         keras_kepala = kwargs.get('keras_kepala')
    #         kreatif = kwargs.get('kreatif')
    #         mudah_akrab = kwargs.get('mudah_akrab')
    #         mudah_bergaul = kwargs.get('mudah_bergaul')
    #         berjiwa_pengasuh = kwargs.get('berjiwa_pengasuh')
    #         pandai = kwargs.get('pandai')
    #         patuh = kwargs.get('patuh')
    #         pemaaf = kwargs.get('pemaaf')
    #         penakut = kwargs.get('penakut')
    #         pemalu = kwargs.get('pemalu')
    #         pemarah = kwargs.get('pemarah')
    #         pembangkang = kwargs.get('pembangkang')
    #         pemberi = kwargs.get('pemberi')
    #         pembohong = kwargs.get('pembohong')
    #         pemurung = kwargs.get('pemurung')
    #         pemimpin = kwargs.get('pemimpin')
    #         pemelas = kwargs.get('pemelas')
    #         pendiam = kwargs.get('pendiam')
    #         penghayal = kwargs.get('penghayal')
    #         penuh_perhatian = kwargs.get('penuh_perhatian')
    #         penyayang = kwargs.get('penyayang')
    #         penyendiri = kwargs.get('penyendiri')
    #         rajin = kwargs.get('rajin')
    #         sabar = kwargs.get('sabar')
    #         senang_berteman = kwargs.get('senang_berteman')
    #         sensitif = kwargs.get('sensitif')
    #         lainnya = kwargs.get('lainnya')

    #         # TTD fields
    #         hari_pengisian = kwargs.get('hari_pengisian')
    #         tanggal_pengisian = kwargs.get('tanggal_pengisian')
    #         ttd_ayah = kwargs.get('ttd_ayah')
    #         ttd_ibu = kwargs.get('ttd_ibu')

    #         file_akta = request.httprequest.files.get('file_akta')
    #         file_pas_ft = request.httprequest.files.get('file_pas_ft')
    #         file_kk = request.httprequest.files.get('file_kk')
    #         file_ktp_ortu = request.httprequest.files.get('file_ktp_ortu')

    #         file_akta_base64 = base64.b64encode(file_akta.read()) if file_akta else None
    #         file_pas_ft_base64 = base64.b64encode(file_pas_ft.read()) if file_pas_ft else None
    #         file_kk_base64 = base64.b64encode(file_kk.read()) if file_kk else None
    #         file_ktp_ortu_base64 = base64.b64encode(file_ktp_ortu.read()) if file_ktp_ortu else None


    #         # Buat record baru di model formulir.sm
    #         admission = request.env['formulir.tk'].sudo().create({
    #             'register_id': register_id,
    #             'name': name,
    #             'first_name': first_name,
    #             'middle_name': middle_name,
    #             'last_name': last_name,
    #             'gender': gender,
    #             'birth_place': birth_place,
    #             'birth_date': birth_date,
    #             'alamat_siswa': alamat_siswa,
    #             'email': email,
    #             'nisn': nisn,
    #             'nik': nik,
    #             'no_kk': no_kk,
    #             'no_akta_lahir': no_akta_lahir,
    #             'agama': agama,
    #             'kewarganegaraan': kewarganegaraan,
    #             'rt_rw': rt_rw,
    #             'kecamatan_id': kecamatan_id,
    #             'kelurahan_id': kelurahan_id,
    #             'kode_pos': kode_pos,
    #             'tempat_tinggal': tempat_tinggal,
    #             'moda_transport': moda_transport,
    #             'anak_ke': anak_ke,
    #             'punya_kia': punya_kia,
    #             'jenis_ppdb': jenis_ppdb,
    #             'asal_sekolah': asal_sekolah,
    #             'alamat_sekolah': alamat_sekolah,
    #             'ayah_id': ayah_id,
    #             'tempat_lahir_ayah': tempat_lahir_ayah,
    #             'tgl_lahir_ayah': tgl_lahir_ayah,
    #             'telp_ayah': telp_ayah,
    #             'email_ayah': email_ayah,
    #             'suku_ayah': suku_ayah,
    #             'agama_ayah': agama_ayah,
    #             'pendidikan_ayah': pendidikan_ayah,
    #             'pekerjaan_ayah': pekerjaan_ayah,
    #             'jabatan_ayah': jabatan_ayah,
    #             'penghasilan_ayah': penghasilan_ayah,
    #             'tanggungan_ayah': tanggungan_ayah,
    #             'status_ayah': status_ayah,
    #             'alamat_ayah': alamat_ayah,
    #             'ibu_id': ibu_id,
    #             'tempat_lahir_ibu': tempat_lahir_ibu,
    #             'tgl_lahir_ibu': tgl_lahir_ibu,
    #             'telp_ibu': telp_ibu,
    #             'email_ibu': email_ibu,
    #             'suku_ibu': suku_ibu,
    #             'agama_ibu': agama_ibu,
    #             'pendidikan_ibu': pendidikan_ibu,
    #             'pekerjaan_ibu': pekerjaan_ibu,
    #             'jabatan_ibu': jabatan_ibu,
    #             'penghasilan_ibu': penghasilan_ibu,
    #             'tanggungan_ibu': tanggungan_ibu,
    #             'status_ibu': status_ibu,
    #             'alamat_ibu': alamat_ibu,
    #             'tinggi_bdn': tinggi_bdn,
    #             'berat_bdn': berat_bdn,
    #             'lingkar_kpl': lingkar_kpl,
    #             'jrk_tmpt_plhn': jrk_tmpt_plhn,
    #             'jrk_tmpt_km': jrk_tmpt_km,
    #             'waktu_tempuh': waktu_tempuh,
    #             'jmlh_saudara_kandung': jmlh_saudara_kandung,
    #             'asi': asi,
    #             'lama_asi': lama_asi,
    #             'susu': susu,
    #             'anak_minum': anak_minum,
    #             'makan_padat': makan_padat,
    #             'favorit': favorit,
    #             'ga_favorit': ga_favorit,
    #             'makan_sendiri': makan_sendiri,
    #             'alergi': alergi,
    #             'tidur': tidur,
    #             'kamar': kamar,
    #             'tempat_tidur': tempat_tidur,
    #             'teman_tidur': teman_tidur,
    #             'jam_tidur': jam_tidur,
    #             'bangun_malam': bangun_malam,
    #             'jam_bangun': jam_bangun,
    #             'tidur_siang': tidur_siang,
    #             'mengantuk': mengantuk,
    #             'kebiasaan_tidur': kebiasaan_tidur,

    #             # Toilet Training Fields
    #             'toilet': toilet,
    #             'berhasil_toilet': berhasil_toilet,
    #             'mulai_toilet': mulai_toilet,
    #             'ngompol': ngompol,
    #             'tidak_ngompol': tidak_ngompol,
    #             'kencing_malam': kencing_malam,
    #             'bantuan_toilet': bantuan_toilet,

    #             # Additional fields for 'Bermain' section
    #             'bermain': bermain,
    #             'teman_main': teman_main,
    #             'orang_rumah': orang_rumah,
    #             'ket_bermain': ket_bermain,
    #             'hubungan_dekat': hubungan_dekat,
    #             'kegiatan_anak': kegiatan_anak,

    #             # Fields for 'Hobi dan Pertemanan'
    #             'hobi_anak': hobi_anak,
    #             'teman_hobi': teman_hobi,
    #             'kecenderungan': kecenderungan,
    #             'teman_sebaya': teman_sebaya,
    #             'hal_disukai': hal_disukai,

    #             # Fields for 'Pembelajaran'
    #             'atmosfer_singkat': atmosfer_singkat,
    #             'sekolah_dicari': sekolah_dicari,
    #             'deskripsi': deskripsi,
    #             'proses_belajar': proses_belajar,
    #             'metode_disiplin': metode_disiplin,
    #             'metode_aturan': metode_aturan,
    #             'metode_pendekatan': metode_pendekatan,

    #             # Fields for 'Temperament'
    #             'agresif': agresif,
    #             'aktif': aktif,
    #             'berani': berani,
    #             'cengeng': cengeng,
    #             'cerewet': cerewet,
    #             'ceria': ceria,
    #             'dominan': dominan,
    #             'pengikut': pengikut,
    #             'humoris': humoris,
    #             'ingin_tahu': ingin_tahu,
    #             'keras_kepala': keras_kepala,
    #             'kreatif': kreatif,
    #             'mudah_akrab': mudah_akrab,
    #             'mudah_bergaul': mudah_bergaul,
    #             'berjiwa_pengasuh': berjiwa_pengasuh,
    #             'pandai': pandai,
    #             'patuh': patuh,
    #             'pemaaf': pemaaf,
    #             'penakut': penakut,
    #             'pemalu': pemalu,
    #             'pemarah': pemarah,
    #             'pembangkang': pembangkang,
    #             'pemberi': pemberi,
    #             'pembohong': pembohong,
    #             'pemurung': pemurung,
    #             'pemimpin': pemimpin,
    #             'pemelas': pemelas,
    #             'pendiam': pendiam,
    #             'penghayal': penghayal,
    #             'penuh_perhatian': penuh_perhatian,
    #             'penyayang': penyayang,
    #             'penyendiri': penyendiri,
    #             'rajin': rajin,
    #             'sabar': sabar,
    #             'senang_berteman': senang_berteman,
    #             'sensitif': sensitif,
    #             'lainnya': lainnya,

    #             # TTD fields
    #             'hari_pengisian': hari_pengisian,
    #             'tanggal_pengisian': tanggal_pengisian,
    #             'ttd_ayah': ttd_ayah,
    #             'ttd_ibu': ttd_ibu,
    #         })
            
    #         return {
    #             'status': 200,
    #             'message': 'Admission created successfully',
    #             'admission_id': admission.id
    #         }
    #     except Exception as e:
    #         return {
    #             'status': 500,
    #             'message': str(e)
    #         }



