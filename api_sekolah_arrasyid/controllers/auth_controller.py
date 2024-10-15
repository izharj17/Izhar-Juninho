from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
import json
from werkzeug.exceptions import Unauthorized

class AuthController(http.Controller):


    @http.route('/api/login', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        try:
            request.session.authenticate(db, login, password)
            user = request.env.user
            if user:
                result = request.env['ir.http'].session_info()
                result['tipe_user'] = user.tipe_user
                return result
            else:
                raise Unauthorized()
        except AccessDenied:
            return Unauthorized('Invalid credentials or unauthorized access.')
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 200,
                    'message': 'Internal Server Error',
                    'data': {'message': str(e)}
                }
            }

            
    @http.route('/api/logout', type='json', auth="user")
    def destroy(self):
        request.session.logout()

    # @http.route('/api/logout', type='json', auth="user")
    # def destroy(self, db, session_id):
    #     try:
    #         # Authenticate with the provided database and session_id
    #         request.session.authenticate(db, session_id, '')
    #         request.session.logout()
    #         return {'result': 'Logged out successfully'}
    #     except Exception as e:
    #         return {
    #             'jsonrpc': '2.0',
    #             'error': {
    #                 'code': 500,
    #                 'message': 'Failed to logout',
    #                 'data': {'message': str(e)}
    #             }
    #         }

    