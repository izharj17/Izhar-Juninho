from odoo import http
from odoo.http import request, Response
import json

class ReportController(http.Controller):

    @http.route('/api/classyear', type='http', auth='user', methods=['GET'])
    def get_child_reports(self):
        user = request.env.user
        parent = request.env['op.parent'].sudo().search([('user_id', '=', user.id)], limit=1)

        if not parent:
            return Response(json.dumps({"error": "Parent not found"}), status=404, mimetype='application/json')

        children = parent.student_ids

        if not children:
            return Response(json.dumps({"error": "No children found for this parent"}), status=404, mimetype='application/json')

        class_set = set()
        year_set = set()
        reports_data = {'classes': [], 'academic_years': []}

        for child in children:
            raport_records = request.env['raport.siswa.sts'].sudo().search([('student_id', '=', child.id)])
            for report in raport_records:
                class_info = (report.kelas_id.id, report.kelas_id.name)
                academic_year_info = (report.tahun_pelajaran.id, report.tahun_pelajaran.name)

                if class_info not in class_set:
                    class_set.add(class_info)
                    reports_data['classes'].append({
                        'class_id': report.kelas_id.id,
                        'class_name': report.kelas_id.name
                    })

                if academic_year_info not in year_set:
                    year_set.add(academic_year_info)
                    reports_data['academic_years'].append({
                        'academic_year_id': report.tahun_pelajaran.id,
                        'academic_year_name': report.tahun_pelajaran.name
                    })

        return Response(json.dumps({
            'status': 'success',
            'data': reports_data
        }), mimetype='application/json')


    # @http.route('/api/search_raport', type='json', auth='user', methods=['POST'], csrf=False)
    # def search_raport(self, **kwargs):
    #     try:
    #         data = request.jsonrequest

    #         student_id = data.get('student_id')
    #         kelas_id = data.get('kelas_id')
    #         semester_id = data.get('semester_id')
    #         tahun_pelajaran = data.get('tahun_pelajaran')
    #         jenis_raport = data.get('jenis_raport')

    #         domain = []

    #         if student_id:
    #             domain.append(('student_id', '=', student_id))
    #         if kelas_id:
    #             domain.append(('kelas_id', '=', kelas_id))
    #         if semester_id:
    #             domain.append(('semester_id', '=', semester_id))
    #         if tahun_pelajaran:
    #             domain.append(('tahun_pelajaran', '=', tahun_pelajaran))
    #         if jenis_raport:
    #             domain.append(('jenis_raport', '=', jenis_raport))

    #         raports = request.env['raport.siswa.sts'].sudo().search(domain)

    #         raport_data = []
    #         for raport in raports:
    #             raport_data.append({
    #                 'id': raport.id,
    #                 'kode_seq': raport.kode_seq,
    #                 'jenis_raport': raport.jenis_raport,
    #                 'student_id': {
    #                     'id': raport.student_id.id,
    #                     'name': raport.student_id.name,
    #                     'nis_nisn': raport.nis_nisn,
    #                 },
    #                 'sekolah_id': {
    #                     'id': raport.sekolah_id.id,
    #                     'name': raport.sekolah_id.name,
    #                     'alamat_sekolah': raport.alamat_sekolah,
    #                 },
    #                 'kelas_id': {
    #                     'id': raport.kelas_id.id,
    #                     'name': raport.kelas_id.name,
    #                 },
    #                 'grade_id': {
    #                     'id': raport.grade_id.id,
    #                     'name': raport.grade_id.name,
    #                 },
    #                 'semester_id': raport.semester_id,
    #                 'tahun_pelajaran': {
    #                     'id': raport.tahun_pelajaran.id,
    #                     'name': raport.tahun_pelajaran.name,
    #                 },
    #                 'jenis_raport':raport.jenis_raport,
    #                 'state': raport.state,
    #                 'created_at': raport.create_date,
    #                 'updated_at': raport.write_date,
    #                 'tinggi_bdn': raport.tinggi_bdn,
    #                 'berat_bdn': raport.berat_bdn,
    #                 'lingkar_kpl': raport.lingkar_kpl,
    #                 'pendengaran': raport.pendengaran,
    #                 'penglihatan': raport.penglihatan,
    #                 'gigi': raport.gigi,
    #                 'sakit': raport.sakit,
    #                 'ijin': raport.ijin,
    #                 'tanpa_ket': raport.tanpa_ket,
    #                 'mandiri': raport.mandiri,
    #                 'disiplin': raport.disiplin,
    #                 'tertib': raport.tertib,
    #                 'percaya_diri': raport.percaya_diri,
    #                 'tanggung_jawab': raport.tanggung_jawab,
    #                 'kerjasama': raport.kerjasama,
    #                 'kepemimpinan': raport.kepemimpinan,
    #                 'ksmpln_saran': raport.ksmpln_saran,
    #                 'keputusan_siswa': raport.keputusan_siswa,
    #                 'ttd_ortu': raport.ttd_ortu,
    #                 'ttd_walas': raport.ttd_walas,
    #                 'ttd_kepsek': raport.ttd_kepsek,
    #                 'raport_siswa_ids': [{
    #                     'subject_id': line.subject_id.id,
    #                     'subject_name': line.subject_id.name,
    #                     'nilai_akhir': line.nilai_akhir,
    #                     'note': line.note,
    #                     'note2': line.note2,
    #                 } for line in raport.raport_siswa_ids],
    #                 'mulok_siswa_ids': [{
    #                     'student_id': line.student_id.id,
    #                     'student_name': line.student_id.name,
    #                     'subject_id': line.subject_id.id,
    #                     'subject_name': line.subject_id.name,
    #                     'nis_nisn': line.nis_nisn,
    #                     'semester_id': line.semester_id,
    #                     'tahun_pelajaran': line.tahun_pelajaran.id,
    #                     'nilai_akhir': line.nilai_akhir,
    #                     'note': line.note,
    #                     'note2': line.note2,
    #                 } for line in raport.mulok_siswa_ids],
    #                 'prestasi_siswa_ids': [{
    #                     'nama': line.nama,
    #                     'student_id': line.student_id.id,
    #                     'student_name': line.student_id.name,
    #                     'nis_nisn': line.nis_nisn,
    #                     'instansi': line.instansi,
    #                     'url': line.url,
    #                     'semester_id': line.semester_id,
    #                     'tahun_pelajaran': line.tahun_pelajaran.id,
    #                     'note': line.note,
    #                 } for line in raport.prestasi_siswa_ids],
    #                 'kegiatan_siswa_ids': [{
    #                     'nama': line.nama,
    #                     'deskripsi': line.deskripsi,
    #                 } for line in raport.kegiatan_siswa_ids],
    #             })

    #         return {
    #             'status': 200,
    #             'message': 'Raport data retrieved successfully',
    #             'data': raport_data
    #         }

    #     except Exception as e:
    #         return {
    #             'status': 500,
    #             'message': str(e)
    #         }

    
    @http.route('/api/search_raport', type='json', auth='user', methods=['POST'], csrf=False)
    def search_raport(self, **kwargs):
        try:
            data = request.jsonrequest

            student_id = data.get('student_id')
            kelas_id = data.get('kelas_id')
            semester_id = data.get('semester_id')
            tahun_pelajaran = data.get('tahun_pelajaran')
            jenis_raport = data.get('jenis_raport')

            domain = []

            if student_id:
                domain.append(('student_id', '=', student_id))
            if kelas_id:
                domain.append(('kelas_id', '=', kelas_id))
            if semester_id:
                domain.append(('semester_id', '=', semester_id))
            if tahun_pelajaran:
                domain.append(('tahun_pelajaran', '=', tahun_pelajaran))
            if jenis_raport:
                domain.append(('jenis_raport', '=', jenis_raport))

            raports = request.env['raport.siswa.sts'].sudo().search(domain)

            raport_data = []
            for raport in raports:
                raport_data.append({
                    'id': raport.id or None,
                    'kode_seq': raport.kode_seq or None,
                    'jenis_raport': raport.jenis_raport or None,
                    'student_id': {
                        'id': raport.student_id.id or None,
                        'name': raport.student_id.name or None,
                        'nis_nisn': raport.nis_nisn or None,
                    },
                    'sekolah_id': {
                        'id': raport.sekolah_id.id or None,
                        'name': raport.sekolah_id.name or None,
                        'alamat_sekolah': raport.alamat_sekolah or None,
                    },
                    'kelas_id': {
                        'id': raport.kelas_id.id or None,
                        'name': raport.kelas_id.name or None,
                    },
                    'grade_id': {
                        'id': raport.grade_id.id or None,
                        'name': raport.grade_id.name or None,
                    },
                    'semester_id': raport.semester_id or None,
                    'tahun_pelajaran': {
                        'id': raport.tahun_pelajaran.id or None,
                        'name': raport.tahun_pelajaran.name or None,
                    },
                    'jenis_raport': raport.jenis_raport or None,
                    'state': raport.state or None,
                    'created_at': raport.create_date or None,
                    'updated_at': raport.write_date or None,
                    'tinggi_bdn': raport.tinggi_bdn or None,
                    'berat_bdn': raport.berat_bdn or None,
                    'lingkar_kpl': raport.lingkar_kpl or None,
                    'pendengaran': raport.pendengaran or None,
                    'penglihatan': raport.penglihatan or None,
                    'gigi': raport.gigi or None,
                    'sakit': raport.sakit or None,
                    'ijin': raport.ijin or None,
                    'tanpa_ket': raport.tanpa_ket or None,
                    'mandiri': raport.mandiri or None,
                    'disiplin': raport.disiplin or None,
                    'tertib': raport.tertib or None,
                    'percaya_diri': raport.percaya_diri or None,
                    'tanggung_jawab': raport.tanggung_jawab or None,
                    'kerjasama': raport.kerjasama or None,
                    'kepemimpinan': raport.kepemimpinan or None,
                    'ksmpln_saran': raport.ksmpln_saran or None,
                    'keputusan_siswa': raport.keputusan_siswa or None,
                    'ttd_ortu': raport.ttd_ortu or None,
                    'ttd_walas': raport.ttd_walas or None,
                    'ttd_kepsek': raport.ttd_kepsek or None,
                    'raport_siswa_ids': [{
                        'subject_id': line.subject_id.id or None,
                        'subject_name': line.subject_id.name or None,
                        'nilai_akhir': line.nilai_akhir or None,
                        'note': line.note or None,
                        'note2': line.note2 or None,
                    } for line in raport.raport_siswa_ids],
                    'mulok_siswa_ids': [{
                        'student_id': line.student_id.id or None,
                        'student_name': line.student_id.name or None,
                        'subject_id': line.subject_id.id or None,
                        'subject_name': line.subject_id.name or None,
                        'nis_nisn': line.nis_nisn or None,
                        'semester_id': line.semester_id or None,
                        'tahun_pelajaran': line.tahun_pelajaran.id or None,
                        'nilai_akhir': line.nilai_akhir or None,
                        'note': line.note or None,
                        'note2': line.note2 or None,
                    } for line in raport.mulok_siswa_ids],
                    'prestasi_siswa_ids': [{
                        'nama': line.nama or None,
                        'student_id': line.student_id.id or None,
                        'student_name': line.student_id.name or None,
                        'nis_nisn': line.nis_nisn or None,
                        'instansi': line.instansi or None,
                        'url': line.url or None,
                        'semester_id': line.semester_id or None,
                        'tahun_pelajaran': line.tahun_pelajaran.id or None,
                        'note': line.note or None,
                    } for line in raport.prestasi_siswa_ids],
                    'kegiatan_siswa_ids': [{
                        'nama': line.nama or None,
                        'deskripsi': line.deskripsi or None,
                    } for line in raport.kegiatan_siswa_ids],
                })

            return {
                'status': 200,
                'message': 'Raport data retrieved successfully',
                'data': raport_data
            }

        except Exception as e:
            return {
                'status': 500,
                'message': str(e)
            }
