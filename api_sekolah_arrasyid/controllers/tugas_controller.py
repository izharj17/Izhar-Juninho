from odoo import http, fields
from odoo.http import request, Response
from odoo.exceptions import AccessError
import json
import base64
from werkzeug.exceptions import BadRequest


class OpAssignmentAPI(http.Controller):

    @http.route('/api/op_assignment', type='json', auth='user')
    def get_op_assignments(self):
        try:
            assignments = request.env['op.assignment'].sudo().search([])
            data = []
            for assignment in assignments:
                data.append({
                    'name': assignment.grading_assignment_id.name,
                    'issued_date': assignment.grading_assignment_id.issued_date,
                })
            return {'success': True, 'data': data}
        except AccessError:
            return {'success': False, 'message': 'Access Denied'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
    @http.route('/api/op_assignment/user', type='json', auth='user')
    def get_user_assignments(self):
        try:
            # Get the current user from the session
            current_user = request.env.user

            # Search for the student's record using the current user's partner ID
            student = request.env['op.student'].sudo().search([('partner_id', '=', current_user.partner_id.id)], limit=1)
            if not student:
                return {'success': False, 'message': 'User is not associated with any student record'}

            # Fetch assignments allocated to the student
            assignments = request.env['op.assignment'].sudo().search([('allocation_ids', 'in', [student.id])])
            
            data = []
            for assignment in assignments:
                data.append({
                    'name': assignment.grading_assignment_id.name,
                    'issued_date': assignment.grading_assignment_id.issued_date,
                })

            return {'success': True, 'data': data}
        except AccessError:
            return {'success': False, 'message': 'Access Denied'}
        except Exception as e:
            return {'success': False, 'message': str(e)}


    # @http.route('/api/assignment_user', auth='user', methods=['GET'], type='http', csrf=False)
    # def get_assignments(self, **kwargs):
    #     try:
    #         user = request.env.user

    #         student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

    #         if not student:
    #             return Response(json.dumps({"error": "Student not found"}), status=404, mimetype='application/json')

    #         assignments = request.env['op.assignment'].sudo().search([('allocation_ids', 'in', [student.id])])

    #         if assignments:
    #             assignment_data = []
    #             for assignment in assignments:
    #                 sub_lines = request.env['op.assignment.sub.line'].sudo().search([
    #                     ('assignment_id', '=', assignment.id),
    #                     ('student_id', '=', student.id)
    #                 ])
    #                 if sub_lines:
    #                     continue

    #                 submission_date = assignment.submission_date.strftime('%Y-%m-%d %H:%M:%S') if assignment.submission_date else None
    #                 subject_name = assignment.grading_assignment_id.subject_id.name if assignment.grading_assignment_id.subject_id else "N/A"
                    
    #                 assignment_data.append({
    #                     'assignment_id': assignment.id,
    #                     'description': assignment.description,
    #                     'submission_date': submission_date,
    #                     'assignment_name': assignment.grading_assignment_id.name,
    #                     'subject_name': subject_name,
    #                 })

    #             if assignment_data:
    #                 response_data = {
    #                     'status': 200,
    #                     'assignment_count': len(assignment_data),
    #                     'assignments': assignment_data
    #                 }
    #                 return Response(json.dumps(response_data), status=200, mimetype='application/json')
    #             else:
    #                 return Response(json.dumps({"error": "No assignments found for the student"}), status=404, mimetype='application/json')

    #     except Exception as e:
    #         return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
    
    @http.route('/api/assignment_user', auth='user', methods=['GET'], type='http', csrf=False)
    def get_assignments(self, **kwargs):
        try:
            user = request.env.user

            student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

            if not student:
                return Response(json.dumps({"error": "Student not found"}), status=404, mimetype='application/json')

            assignments = request.env['op.assignment'].sudo().search([
                ('allocation_ids', 'in', [student.id]),
                ('state', 'in', ['publish', 'finish'])
            ])

            if assignments:
                assignment_data = []
                for assignment in assignments:
                    sub_lines = request.env['op.assignment.sub.line'].sudo().search([
                        ('assignment_id', '=', assignment.id),
                        ('student_id', '=', student.id)
                    ])
                    if sub_lines:
                        continue

                    submission_date = assignment.submission_date.strftime('%Y-%m-%d %H:%M:%S') if assignment.submission_date else None
                    subject_name = assignment.grading_assignment_id.subject_id.name if assignment.grading_assignment_id.subject_id else "N/A"
                    
                    assignment_data.append({
                        'assignment_id': assignment.id,
                        'description': assignment.description,
                        'submission_date': submission_date,
                        'assignment_name': assignment.grading_assignment_id.name,
                        'subject_name': subject_name,
                    })

                if assignment_data:
                    response_data = {
                        'status': 200,
                        'assignment_count': len(assignment_data),
                        'assignments': assignment_data
                    }
                    return Response(json.dumps(response_data), status=200, mimetype='application/json')
                else:
                    return Response(json.dumps({"error": "No assignments found for the student"}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')



    @http.route('/api/assignment_user_batch', auth='user', methods=['GET'], type='http', csrf=False)
    def get_assignments_batch(self, **kwargs):
        try:
            user = request.env.user

            # Get the student record for the logged-in user
            student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

            if not student:
                return Response(json.dumps({"error": "Student not found"}), status=404, mimetype='application/json')


            # Get the batch ID from the op.student.course model
            student_course = request.env['op.student.course'].sudo().search([('student_id', '=', student.id)], limit=1)
            if not student_course:
                return Response(json.dumps({"error": "Student course details not found"}), status=404, mimetype='application/json')

            batch_id = student_course.batch_id.id

            # Search for assignments allocated to the student's batch and with the correct state
            assignments = request.env['op.assignment'].sudo().search([
                ('batch_id', '=', batch_id),
                ('allocation_ids', 'in', [student.id]),
                ('state', 'in', ['publish', 'finish'])
            ])

            if assignments:
                assignment_data = []
                for assignment in assignments:
                    sub_lines = request.env['op.assignment.sub.line'].sudo().search([
                        ('assignment_id', '=', assignment.id),
                        ('student_id', '=', student.id)
                    ])
                    if sub_lines:
                        continue

                    submission_date = assignment.submission_date.strftime('%Y-%m-%d') if assignment.submission_date else None
                    subject_name = assignment.grading_assignment_id.subject_id.name if assignment.grading_assignment_id.subject_id else "N/A"
                    
                    assignment_data.append({
                        'assignment_id': assignment.id,
                        'description': assignment.description,
                        'submission_date': submission_date,
                        'assignment_name': assignment.grading_assignment_id.name,
                        'subject_name': subject_name,
                        
                    })

                if assignment_data:
                    response_data = {
                        'status': 200,
                        'assignment_count': len(assignment_data),
                        'assignments': assignment_data
                    }
                    return Response(json.dumps(response_data), status=200, mimetype='application/json')
                else:
                    return Response(json.dumps({"error": "No assignments found for the student"}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')





    @http.route('/api/assignment_count', auth='user', methods=['GET'], type='json', csrf=False)
    def get_assignment_count(self, **kwargs):
        try:
            user = request.env.user

            student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

            if not student:
                return {
                    'status': 404,
                    'error': 'Student not found'
                }

            assignment_count = request.env['op.assignment'].sudo().search_count([('allocation_ids', 'in', [student.id])])

            return {
                'status': 200,
                'assignment_count': assignment_count
            }

        except Exception as e:
            return {
                'status': 500,
                'error': str(e)
            }


    @http.route('/api/submit_assignment', type='http', auth="user", methods=['POST'], csrf=False)
    def submit_assignment(self, **kwargs):
        try:
            assignment_id = kwargs.get('assignment_id')
            # description = kwargs.get('description')
            file = request.httprequest.files.get('file')

            student = request.env['op.student'].sudo().search([('user_id', '=', request.env.uid)], limit=1)
            if not student:
                return request.make_response(json.dumps({'status': 400, 'message': 'Student not found'}), headers={'Content-Type': 'application/json'})

            assignment = request.env['op.assignment'].sudo().browse(assignment_id)
            if not assignment:
                return request.make_response(json.dumps({'status': 404, 'message': 'Assignment not found'}), headers={'Content-Type': 'application/json'})

            attachment_url = None
            if file:
                file_content = file.read()
                file_base64 = base64.b64encode(file_content)
                file_name = file.filename

                attachment = request.env['ir.attachment'].sudo().create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': file_base64,
                    'res_model': 'op.assignment.sub.line',
                    'res_id': 0,
                    'mimetype': file.content_type,
                    'public': True, 
                })

                # attachment_url = f'/web/content/{attachment.id}?download=true'
                # attachment_url = f'/web/image/{attachment.id}/{attachment.name}'
                base_url = request.httprequest.host_url

                attachment_url = f'{base_url}web/image/{attachment.id}/{attachment.name}'


            submission = request.env['op.assignment.sub.line'].sudo().create({
                'assignment_id': assignment.id,
                'student_id': student.id,
                # 'description': description,
                'state': 'submit',
                'submission_date': fields.Datetime.now(),
                'attachment': attachment_url,
            })

            if file:
                attachment.write({'res_id': submission.id})

            return request.make_response(json.dumps({'status': 200, 'message': 'Assignment submitted successfully', 'submission_id': submission.id, 'attachment_url': attachment_url}), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})

        

    @http.route('/api/submitted_assignments', auth='user', methods=['GET'], type='http', csrf=False)
    def get_submitted_assignments(self, **kwargs):
        try:
            user = request.env.user
            student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

            if not student:
                return Response(json.dumps({"error": "Student not found"}), status=404, mimetype='application/json')

            submitted_assignments = request.env['op.assignment.sub.line'].sudo().search([
                ('student_id', '=', student.id),
                ('state', 'in', ['submit', 'accept'])
            ])

            if submitted_assignments:
                assignment_data = []
                for sub_line in submitted_assignments:
                    marks = sub_line.marks if sub_line.state == 'accept' else 0.0

                    submission_date = sub_line.submission_date.strftime('%Y-%m-%d %H:%M:%S') if sub_line.submission_date else None
                    subject_name = sub_line.assignment_id.grading_assignment_id.subject_id.name if sub_line.assignment_id.grading_assignment_id.subject_id else "N/A"
                    
                    assignment_data.append({
                        'assignment_id': sub_line.assignment_id.id,
                        'assignment_name': sub_line.assignment_id.grading_assignment_id.name,
                        'description': sub_line.description,
                        'submission_date': submission_date,
                        'marks': marks,
                        'state': sub_line.state,
                        'note': sub_line.note,
                        'attachment': sub_line.attachment,
                        'subject_name': subject_name,
                    })

                response_data = {
                    'status': 200,
                    'submitted_assignment_count': len(assignment_data),
                    'submitted_assignments': assignment_data
                }
                return Response(json.dumps(response_data), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"error": "No submitted assignments found for the student"}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')

        
    @http.route('/api/submitted_assignments_batch', auth='user', methods=['GET'], type='http', csrf=False)
    def get_submitted_assignments_batch(self, **kwargs):
        try:
            user = request.env.user
            student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

            if not student:
                return Response(json.dumps({"error": "Student not found"}), status=404, mimetype='application/json')

            # Get the batch ID from the op.student.course model
            student_course = request.env['op.student.course'].sudo().search([('student_id', '=', student.id)], limit=1)
            if not student_course:
                return Response(json.dumps({"error": "Student course details not found"}), status=404, mimetype='application/json')

            batch_id = student_course.batch_id.id

            # Filter the submitted assignments by batch ID and student ID
            submitted_assignments = request.env['op.assignment.sub.line'].sudo().search([
                ('student_id', '=', student.id),
                ('assignment_id.batch_id', '=', batch_id),
                ('state', 'in', ['submit', 'accept'])
            ])

            if submitted_assignments:
                assignment_data = []
                for sub_line in submitted_assignments:
                    marks = sub_line.marks if sub_line.state == 'accept' else 0.0

                    submission_date = sub_line.submission_date.strftime('%Y-%m-%d %H:%M:%S') if sub_line.submission_date else None
                    subject_name = sub_line.assignment_id.grading_assignment_id.subject_id.name if sub_line.assignment_id.grading_assignment_id.subject_id else "N/A"
                    
                    assignment_data.append({
                        'assignment_id': sub_line.assignment_id.id,
                        'assignment_name': sub_line.assignment_id.grading_assignment_id.name,
                        'description': sub_line.description,
                        'submission_date': submission_date,
                        'marks': marks,
                        'state': sub_line.state,
                        'note': sub_line.note,
                        'attachment': sub_line.attachment,
                        'subject_name': subject_name,
                    })

                response_data = {
                    'status': 200,
                    'submitted_assignment_count': len(assignment_data),
                    'submitted_assignments': assignment_data
                }
                return Response(json.dumps(response_data), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"error": "No submitted assignments found for the student"}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')

    
    @http.route('/api/submitted_assignments_children', auth='user', methods=['GET'], type='http', csrf=False)
    def get_submitted_assignments_children(self, **kwargs):
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

            if not students:
                return Response(json.dumps({"error": "No students found for this parent"}), status=404, mimetype='application/json')

            submitted_assignments_data = []

            for student in students:
                # Get the batch ID for the student
                student_course = request.env['op.student.course'].sudo().search([('student_id', '=', student.id)], limit=1)
                if not student_course:
                    continue
                batch_id = student_course.batch_id.id

                # Search for submitted assignments for the student with matching batch ID
                submitted_assignments = request.env['op.assignment.sub.line'].sudo().search([
                    ('student_id', '=', student.id),
                    ('assignment_id.batch_id', '=', batch_id),
                    ('state', 'in', ['submit', 'accept'])
                ])

                if submitted_assignments:
                    for sub_line in submitted_assignments:
                        marks = sub_line.marks if sub_line.state == 'accept' else 0.0

                        submission_date = sub_line.submission_date.strftime('%Y-%m-%d %H:%M:%S') if sub_line.submission_date else None
                        subject_name = sub_line.assignment_id.grading_assignment_id.subject_id.name if sub_line.assignment_id.grading_assignment_id.subject_id else "N/A"

                        assignment_data = {
                            'student_name': student.name,
                            'assignment_id': sub_line.assignment_id.id,
                            'assignment_name': sub_line.assignment_id.grading_assignment_id.name,
                            'description': sub_line.description,
                            'submission_date': submission_date,
                            'marks': marks,
                            'state': sub_line.state,
                            'note': sub_line.note,
                            'attachment': sub_line.attachment,
                            'subject_name': subject_name,
                        }

                        submitted_assignments_data.append(assignment_data)

            if submitted_assignments_data:
                response_data = {
                    'status': 200,
                    'submitted_assignment_count': len(submitted_assignments_data),
                    'submitted_assignments': submitted_assignments_data
                }
                return Response(json.dumps(response_data), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"error": "No submitted assignments found for the students"}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')