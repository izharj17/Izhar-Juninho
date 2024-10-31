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
