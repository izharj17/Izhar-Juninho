# routes.py di Odoo
from odoo import http
from odoo.http import request, Response

class ContactsController(http.Controller):
    @http.route('/api/contact', type='json', auth='public', methods=['POST'], csrf=False)
    def create_contact(self, **kw):
        if 'name' in kw and 'phone' in kw:
            partner = request.env['res.partner'].sudo().create({
                'name': kw.get('name'),
                'phone': kw.get('phone'),
            })
            return {'success': True, 'id': partner.id}
        return {'success': False, 'message': 'Missing required fields'}

     
