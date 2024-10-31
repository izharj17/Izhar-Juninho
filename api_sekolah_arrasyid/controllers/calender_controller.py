from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime, timedelta


class CalendarController(http.Controller):
    @http.route('/api/get_calendar_events', type='http', auth='user', methods=['GET'], csrf=False)
    def get_calendar_events(self, **kwargs):
        try:
            user_id = request.env.user.id

            # Fetch all public calendar events or events the user is invited to
            events = request.env['calendar.event'].sudo().search([
                '|',
                ('privacy', '=', 'public'),
                ('attendee_ids.partner_id.user_ids', 'in', user_id)
            ])

            event_data = []
            for event in events:
                event_data.append({
                    'id': event.id,
                    'name': event.name,
                    'start': event.start.strftime('%Y-%m-%d %H:%M:%S') if event.start else None,
                    'stop': event.stop.strftime('%Y-%m-%d %H:%M:%S') if event.stop else None,
                    'allday': event.allday,
                    'location': event.location,
                    'description': event.description,
                    'attendees': [{'id': attendee.id, 'name': attendee.partner_id.name} for attendee in event.attendee_ids],
                    'show_as': event.show_as,
                    'privacy': event.privacy,
                })

            response_data = {
                'status': 200,
                'message': 'Calendar events retrieved successfully',
                'data': event_data
            }
            return Response(json.dumps(response_data), content_type='application/json', status=200)

        except Exception as e:
            error_data = {
                'status': 500,
                'message': str(e)
            }
            return Response(json.dumps(error_data), content_type='application/json', status=500)
