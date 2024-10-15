from odoo import http
from odoo.http import request, Response
import json

class InvoiceController(http.Controller):

    @http.route('/api/get_invoices', type='http', auth='user', methods=['GET'], csrf=False)
    def get_invoices(self, **kwargs):
        try:
            
            user = request.env.user

            
            parent = request.env['op.parent'].sudo().search([('user_id', '=', user.id)], limit=1)
            if not parent:
                return Response(json.dumps({'status': 403, 'message': 'User is not a parent'}), status=403, mimetype='application/json')

            
            students = parent.student_ids

            invoice_data = []
            for student in students:
                
                partner_id = student.partner_id.id

                
                account_moves = request.env['account.move'].sudo().search([('partner_id', '=', partner_id)])

                for move in account_moves:
                    amount_residual = move.amount_residual if move.payment_state != 'paid' else 0.0
                    date_due = move.invoice_date_due.strftime('%Y-%m-%d') if move.invoice_date_due else None
                    invoice_data.append({
                        'name': move.name,
                        'amount_total': move.amount_total,
                        'amount_residual': amount_residual,
                        'payment_state': move.payment_state,
                        'date_due': date_due,
                    })

            return Response(json.dumps({'status': 200, 'data': invoice_data}), status=200, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({'status': 500, 'message': str(e)}), status=500, mimetype='application/json')
