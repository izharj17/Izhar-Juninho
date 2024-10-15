from odoo import http, fields
from odoo.http import request, Response
from odoo.exceptions import AccessError
import json
from datetime import datetime, timedelta


class ActivityController(http.Controller):

    @http.route('/api/get_activities', type='http', auth='user', methods=['GET'], csrf=False)
    def get_activities(self, **kwargs):
        try:
            user = request.env.user

            parent = request.env['op.parent'].sudo().search([('user_id', '=', user.id)], limit=1)

            if not parent:
                return Response(json.dumps({"error": "Parent not found"}), status=404, mimetype='application/json')

            students = parent.student_ids

            if not students:
                return Response(json.dumps({"error": "No students found for this parent"}), status=404, mimetype='application/json')

            activity_data = []
            for student in students:
                activities = request.env['op.activity'].sudo().search([
                    ('student_id', '=', student.id),
                ], limit=1)
                if activities:
                    for activity in activities:
                        activity_data.append({
                            'id': activity.id,
                            'student_id': {
                                'id': activity.student_id.id,
                                'name': activity.student_id.name,
                            },
                            'faculty_id': {
                                'id': activity.faculty_id.id,
                                'name': activity.faculty_id.name,
                            } if activity.faculty_id else None,
                            'type_id': {
                                'id': activity.type_id.id,
                                'name': activity.type_id.name,
                            } if activity.type_id else None,
                            'description': activity.description,
                            'komen_ortu': activity.komen_ortu,
                            'date': activity.date.strftime('%Y-%m-%d'),
                            'active': activity.active,
                        })
            if activity_data:
                response_data = {
                    'status': 200,
                    'submitted_assignment_count': len(activity_data),
                    'submitted_assignments': activity_data
                }
                return Response(json.dumps(response_data), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"error": "No activity found for the students"}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
