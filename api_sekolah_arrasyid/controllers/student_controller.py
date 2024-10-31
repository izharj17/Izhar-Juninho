from odoo import http
from odoo.http import request, Response
import json

class StudentListController(http.Controller):

    @http.route('/api/student_list', type='http', auth='public', methods=['GET'])
    def student_list(self, **kwargs):
        Student = request.env['op.student']
        students = Student.search([])
        student_data = []
        for student in students:
            student_data.append({
                'name ': student.first_name + student.middle_name + student.last_name
            })
        return Response(json.dumps(student_data), content_type='application/json')


class StudentCountController(http.Controller):

    @http.route('/api/student_count', type='http', auth='public', methods=['GET'])
    def student_count(self, **kwargs):
        Student = request.env['op.student']
        count = Student.search_count([])
        return f"Total number of students: {count}"
    
class StudentPrestasiListController(http.Controller):

    @http.route('/api/student_prestasi_list', type='http', auth='public', methods=['GET'])
    def student_prestasi_list(self, **kwargs):
        StudentPrestasi = request.env['op.student.prestasi']
        prestasis = StudentPrestasi.search([])
        prestasi_data = []
        for prestasi in prestasis:
            prestasi_data.append({
                'nama': prestasi.nama
            })
        return Response(json.dumps(prestasi_data), content_type='application/json')
    
    
class StudentController(http.Controller):

    @http.route('/api/get_students', type='json', auth='user', methods=['GET'])
    def get_students(self):
        students = request.env['op.student'].search([])
        students_data = []
        
        for student in students:
            students_data.append({
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'grade': student.grade.name if student.grade else '',
                'rombel': student.rombel.name if student.rombel else '',
                'birth_date': student.birth_date,
                'age': student.age,
                'birth_place': student.birth_place,
                'nis': student.nis,
                'nisn': student.nisn,
                'blood_group': student.blood_group,
                'gender': student.gender,
                'nationality': student.nationality.name if student.nationality else '',
                'emergency_contact': student.emergency_contact.name if student.emergency_contact else '',
                'visa_info': student.visa_info,
                'id_number': student.id_number,
                'user_id': student.user_id.name if student.user_id else '',
                'gr_no': student.gr_no,
                'category_id': student.category_id.name if student.category_id else '',
                'active': student.active,
                'ayah_id': student.ayah_id.name if student.ayah_id else '',
                'ibu_id': student.ibu_id.name if student.ibu_id else '',
                'wali_id': student.wali_id.name if student.wali_id else '',
                'barcode': student.barcode,
                'nama_panggilan': student.nama_panggilan,
                'no_kk': student.no_kk,
                'nik': student.nik,
                'no_akta_lahir': student.no_akta_lahir,
                'agama': student.agama,
                'kewarganegaraan': student.kewarganegaraan,
                'rt_rw': student.rt_rw,
                'kecamatan_id': student.kecamatan_id.name if student.kecamatan_id else '',
                'kelurahan_id': student.kelurahan_id.name if student.kelurahan_id else '',
                'kode_pos': student.kode_pos,
                'tempat_tinggal': student.tempat_tinggal,
                'moda_transport': student.moda_transport,
                'anak_ke': student.anak_ke,
                'punya_kia': student.punya_kia,
                'tinggi_bdn': student.tinggi_bdn,
                'berat_bdn': student.berat_bdn,
                'lingkar_kpl': student.lingkar_kpl,
                'jrk_tmpt_plhn': student.jrk_tmpt_plhn,
                'jrk_tmpt_km': student.jrk_tmpt_km,
                'waktu_tempuh': student.waktu_tempuh,
                'jmlh_saudara_kandung': student.jmlh_saudara_kandung,
                'graduate': student.graduate,
                'status_graduasi': student.status_graduasi,
            })
        
        return json.dumps({'students': students_data})

    @http.route('/api/student_data', auth='user', methods=['GET'], type='http', csrf=False)
    def get_student_data(self, **kwargs):
        try:
            user = request.env.user

            student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)
            if not student:
                return Response("Student not found", status=404)

            partner = student.partner_id
            kecamatan = student.kecamatan_id
            kelurahan = student.kelurahan_id

            parent_data = []
            for parent in student.parent_ids:
                parent_data.append({
                    'name': parent.name.name,
                    'relationship': parent.relationship_id.name,
                })

            # Extracting father and mother names
            father_name = None
            mother_name = None
            for parent in parent_data:
                if parent['relationship'].lower() == 'ayah':
                    father_name = parent['name']
                elif parent['relationship'].lower() == 'ibu':
                    mother_name = parent['name']

            student_data = {
                'nis': student.nis,
                'nisn': student.nisn,
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'birth_place': student.birth_place,
                'birth_date': student.birth_date.strftime('%Y-%m-%d') if student.birth_date else None,
                'gender': student.gender,
                'nama_panggilan': student.nama_panggilan,
                'agama': student.agama,
                'kewarganegaraan': student.kewarganegaraan,
                'rt_rw': student.rt_rw,
                'kecamatan': kecamatan.name if kecamatan else None,
                'kelurahan': kelurahan.name if kelurahan else None,
                'email': partner.email,
                'mobile': partner.mobile,
                'street': partner.street,
                'city': partner.city,
                'zip': partner.zip,
                'parents': parent_data,
                # 'father_name': father_name,
                # 'mother_name': mother_name,
                'father_name': student.ayah_id.name_ayah if student.ayah_id else '',
                'mother_name': student.ibu_id.name_ibu if student.ibu_id else '',
                'wali_name': student.wali_id.name_wali if student.wali_id else '',
            }
            name_parts = filter(None, [student_data.get('first_name'), student_data.get('middle_name'), student_data.get('last_name')])
            student_data['name'] = " ".join(name_parts)

            agama_mapping = {
                '1': 'Islam',
                '2': 'Kristen',
                '3': 'Katolik',
                '4': 'Hindu',
                '5': 'Budha',
            }

            kewarganegaraan_mapping = {
                '1': 'Indonesia (WNI)',
                '2': 'Asing (WNA)',
            }

            gender_mapping = {
                'm': 'Laki-Laki',
                'f': 'Perempuan',
            }

            if student_data.get('gender'):
                student_data['gender'] = gender_mapping.get(student_data['gender'], student_data['gender'])

            if student_data.get('agama'):
                student_data['agama'] = agama_mapping.get(student_data['agama'], student_data['agama'])

            if student_data.get('kewarganegaraan'):
                student_data['kewarganegaraan'] = kewarganegaraan_mapping.get(student_data['kewarganegaraan'], student_data['kewarganegaraan'])

            address_parts = filter(None, [
                student_data.get('street'),
                student_data.get('rt_rw'),
                student_data.get('kelurahan'),
                student_data.get('kecamatan'),
                student_data.get('city'),
                student_data.get('zip')
            ])
            student_data['address'] = ", ".join(address_parts)

            student_data.pop('street', None)
            student_data.pop('rt_rw', None)
            student_data.pop('kelurahan', None)
            student_data.pop('kecamatan', None)
            student_data.pop('city', None)
            student_data.pop('zip', None)

            student_data.pop('first_name', None)
            student_data.pop('middle_name', None)
            student_data.pop('last_name', None)

            response_data = {
                'status': 200,
                'student': student_data
            }

            return Response(json.dumps(response_data), status=200, mimetype='application/json')

        except Exception as e:
            return Response("An error occurred: %s" % str(e), status=500)
