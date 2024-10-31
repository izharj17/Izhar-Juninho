from odoo import http
from odoo.http import request, Response
import json

class InvoiceController(http.Controller):

    @http.route('/api/get_invoices', type='http', auth='user', methods=['GET'], csrf=False)
    def get_invoices(self, **kwargs):
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

            invoice_data = []
            for student in students:
                # Dapatkan ID partner dari setiap anak
                partner_id = student.partner_id.id

                # Ambil faktur yang terkait dengan ID partner ini
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
