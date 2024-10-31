from odoo import http
from odoo.http import request, Response
import json

class ParentController(http.Controller):

    @http.route('/api/children', auth='user', methods=['GET'], type='http', csrf=False)
    def get_children_data(self, **kwargs):
        try:
            user = request.env.user
            partner = request.env['res.partner'].sudo().search([('user_id', '=', user.id)])

            parent_ayah = request.env['op.data.ayah'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            parent_ibu = request.env['op.data.ibu'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            parent_wali = request.env['op.data.wali'].sudo().search([('partner_id', '=', partner.id)], limit=1)

            if not parent_ayah and not parent_ibu and not parent_wali:
                return Response(json.dumps({'error': 'User is not a parent'}), status=403, mimetype='application/json')

            parent = parent_ayah or parent_ibu or parent_wali

            if not parent:
                return Response(json.dumps({'error': 'User is not a parent'}), status=403, mimetype='application/json')

            students = request.env['op.student'].sudo().search([
                '|', '|',
                ('ayah_id', '=', parent_ayah.id if parent_ayah else 0),
                ('ibu_id', '=', parent_ibu.id if parent_ibu else 0),
                ('wali_id', '=', parent_wali.id if parent_wali else 0)
            ])

            children_data = []
            for student in students:
                partner = student.partner_id
                kecamatan = student.kecamatan_id
                kelurahan = student.kelurahan_id

                student_data = {
                    'id': student.id,
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

                children_data.append(student_data)

            response_data = {
                'status': 200,
                'children': children_data
            }

            return Response(json.dumps(response_data), status=200, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

    # @http.route('/api/parent_data', auth='user', methods=['GET'], type='http', csrf=False)
    # def get_parent_data(self, **kwargs):
    #     try:
    #         user = request.env.user
            
    #         parent = request.env['op.parent'].sudo().search([('user_id', '=', user.id)], limit=1)
    #         if not parent:
    #             return Response("Parent not found", status=404)

    #         partner = parent.name
    #         parent_data = {
    #             'name': parent.name.name,
    #             'student_ids': [{'id': student.id, 'name': student.name} for student in parent.student_ids],
    #             'mobile': parent.mobile,
    #             'email': parent.name.email,
    #             'relationship': parent.relationship_id.name,
    #             'address': {
    #                 'street': partner.street,
    #                 'street2': partner.street2,
    #                 'city': partner.city,
    #                 'state': partner.state_id.name if partner.state_id else None,
    #                 'zip': partner.zip,
    #                 'country': partner.country_id.name if partner.country_id else None
    #             }
    #         }

    #         response_data = {
    #             'status': 200,
    #             'parent': parent_data
    #         }

    #         return Response(json.dumps(response_data), status=200, mimetype='application/json')

    #     except Exception as e:
    #         return Response("An error occurred: %s" % str(e), status=500)

    @http.route('/api/parent_data', auth='user', methods=['GET'], type='http', csrf=False)
    def get_parent_data(self, **kwargs):
        try:
            user = request.env.user
            
            partner = request.env['res.partner'].sudo().search([('user_id', '=', user.id)])
            
            parent_ayah = request.env['op.data.ayah'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            parent_ibu = request.env['op.data.ibu'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            parent_wali = request.env['op.data.wali'].sudo().search([('partner_id', '=', partner.id)], limit=1)

            if not parent_ayah and not parent_ibu and not parent_wali:
                return Response(json.dumps({'error': 'User is not a parent'}), status=403, mimetype='application/json')

            parent = parent_ayah or parent_ibu or parent_wali
            parent_type = 'ayah' if parent_ayah else 'ibu' if parent_ibu else 'wali'

            parent_data = {}
            if parent_type == 'ayah':
                parent_data = {
                    'name': parent.name_ayah,
                    'mobile': str(parent.no_wa) if parent.no_wa else None,
                    'email': parent.email,
                    'relationship': parent.relationship_id.name,
                    'address': {
                        'street': partner.street,
                        'street2': partner.street2,
                        'city': partner.city,
                        'state': partner.state_id.name if partner.state_id else None,
                        'zip': partner.zip,
                        'country': partner.country_id.name if partner.country_id else None
                    },
                    'student_ids': [{'id': student.id, 'name': student.name} for student in parent.student_ayah_ids],
                    'type': 'Ayah'
                }
            elif parent_type == 'ibu':
                parent_data = {
                    'name': parent.name_ibu,
                    'mobile': str(parent.no_wa) if parent.no_wa else None,
                    'email': parent.email,
                    'relationship': parent.relationship_id.name,
                    'address': {
                        'street': partner.street,
                        'street2': partner.street2,
                        'city': partner.city,
                        'state': partner.state_id.name if partner.state_id else None,
                        'zip': partner.zip,
                        'country': partner.country_id.name if partner.country_id else None
                    },
                    'student_ids': [{'id': student.id, 'name': student.name} for student in parent.student_ibu_ids],
                    'type': 'Ibu'
                }
            elif parent_type == 'wali':
                parent_data = {
                    'name': parent.name_wali,
                    'mobile': str(parent.no_wa) if parent.no_wa else None,
                    'email': parent.email,
                    'relationship': parent.relationship_id.name,
                    'address': {
                        'street': partner.street,
                        'street2': partner.street2,
                        'city': partner.city,
                        'state': partner.state_id.name if partner.state_id else None,
                        'zip': partner.zip,
                        'country': partner.country_id.name if partner.country_id else None
                    },
                    'student_ids': [{'id': student.id, 'name': student.name} for student in parent.student_wali_ids],
                    'type': 'Wali'
                }

            response_data = {
                'status': 200,
                'parent': parent_data
            }

            return Response(json.dumps(response_data), status=200, mimetype='application/json')

        except Exception as e:
            return Response("An error occurred: %s" % str(e), status=500)


            
    @http.route('/api/member/profile', type='http', auth='user', methods=['GET'], csrf=False)
    def get_member_profile(self):
        user = request.env['res.users'].sudo().search([('id', '=', request.env.user.id)], limit=1)
        if user:
            member_data = {
                'id': user.id,
                'name': user.name,
                'email': user.login,
                'phone': user.phone,
                'address': user.partner_id.contact_address,
                
            }
            return request.make_response(request.json.encode({'status': 'success', 'data': member_data}), headers={'Content-Type': 'application/json'})
        return request.make_response(request.json.encode({'status': 'error', 'message': 'User not found'}), headers={'Content-Type': 'application/json'})

    


        
