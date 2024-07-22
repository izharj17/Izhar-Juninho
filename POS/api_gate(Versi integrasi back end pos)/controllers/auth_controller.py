from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
import json

class AuthController(http.Controller):

    @http.route('/api/login', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        try:
            request.session.authenticate(db, login, password)
            user = request.env.user
            if user:
                session_info = request.env['ir.http'].session_info()
            
                return session_info
            else:
                raise AccessDenied()
        except AccessDenied:
            return {
                'error': 'Access Denied',
                'message': 'Invalid credentials or unauthorized access.'
            }
        except Exception as e:
            return {
                'error': 'Internal Server Error',
                'message': str(e)
            }
            
    @http.route('/api/logout', type='json', auth="user")
    def destroy(self):
        request.session.logout()

    
class HiWorldController(http.Controller):

    @http.route('/api/hi_world', type='http', auth='public', methods=['GET'])
    def hello_world(self, **kwargs):
        return "Hello, World! hey"