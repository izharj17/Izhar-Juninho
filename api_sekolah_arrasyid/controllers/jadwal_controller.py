from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class OpSessionController(http.Controller):

    @http.route('/api/sessions', type='http', auth='user', methods=['GET'])
    def get_user_sessions(self, month=None, year=None):
        user = request.env.user
        student = request.env['op.student'].sudo().search([('user_id', '=', user.id)], limit=1)

        if not student:
            return Response(json.dumps({"error": "Student not found"}), status=404, mimetype='application/json')

        student_course = request.env['op.student.course'].sudo().search([('student_id', '=', student.id)], limit=1)
        if not student_course:
            return Response(json.dumps({"error": "Student course details not found"}), status=404, mimetype='application/json')

        batch_id = student_course.batch_id.id

        if not batch_id:
            return Response(json.dumps({
                'status': 'error',
                'message': 'User is not associated with any batch.'
            }), status=400, mimetype='application/json')

        domain = [('batch_id', '=', batch_id)]

        if month and year:
            start_date = datetime(year=int(year), month=int(month), day=1)
            end_date = start_date + relativedelta(months=1, days=-1)
            domain.append(('start_datetime', '>=', start_date))
            domain.append(('start_datetime', '<=', end_date))

        sessions = request.env['op.session'].sudo().search(domain)
        sessions_data = []
        for session in sessions:
            timing = session.timing_id

            if timing.am_pm == 'pm' and timing.hour != '12':
                start_hour = int(timing.hour) + 12
            else:
                start_hour = int(timing.hour)

            start_minute = int(timing.minute)
            start_datetime = datetime.combine(session.start_datetime.date(), datetime.min.time())
            start_datetime = start_datetime.replace(hour=start_hour, minute=start_minute)

            end_datetime = start_datetime + timedelta(hours=timing.duration)

            sessions_data.append({
                'name': session.name,
                'start_datetime': start_datetime.isoformat(),
                'end_datetime': end_datetime.isoformat(),
                'course': session.course_id.name,
                'faculty': session.faculty_id.name,
                'subject': session.subject_id.name,
                'batch': session.batch_id.name,
                'classroom': session.classroom_id.name,
                'state': session.state,
            })

        return Response(json.dumps({
            'status': 'success',
            'data': sessions_data
        }), mimetype='application/json')





    @http.route('/api/sessions_parent', type='http', auth='user', methods=['GET'])
    def get_parent_sessions(self, month=None, year=None):
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

            sessions_data = []
            for student in students:
                student_course = request.env['op.student.course'].sudo().search([('student_id', '=', student.id)], limit=1)
                if student_course:
                    batch_id = student_course.batch_id.id
                    
                    # Filter by month and year if provided
                    domain = [('batch_id', '=', batch_id)]
                    if month and year:
                        start_date = f"{int(year):04d}-{int(month):02d}-01"

                        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(months=1) - timedelta(days=1)).strftime("%Y-%m-%d")
                        domain.append(('start_datetime', '>=', start_date))
                        domain.append(('start_datetime', '<=', end_date))
                    
                    sessions = request.env['op.session'].sudo().search(domain)

                    for session in sessions:
                        timing = session.timing_id
                        start_hour = int(timing.hour) if timing.am_pm == 'am' or timing.hour == '12' else int(timing.hour) + 12
                        start_minute = int(timing.minute)
                        start_datetime = datetime.combine(session.start_datetime.date(), datetime.min.time()).replace(hour=start_hour, minute=start_minute)
                        end_datetime = start_datetime + timedelta(hours=timing.duration)

                        sessions_data.append({
                            'name': session.name,
                            'start_datetime': start_datetime.isoformat(),
                            'end_datetime': end_datetime.isoformat(),
                            'course': session.course_id.name,
                            'faculty': session.faculty_id.name,
                            'subject': session.subject_id.name,
                            'batch': session.batch_id.name,
                            'classroom': session.classroom_id.name,
                            'state': session.state,
                            'student_name': student.name
                        })

            return Response(json.dumps({'status': 'success', 'data': sessions_data}), mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


