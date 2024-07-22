# controllers/main.py

from odoo import http
from odoo.http import request, Response
import json

class PosOrderController(http.Controller):

    @http.route('/api/create_order', type='json', auth='user', methods=['POST'])
    def create_order(self, **kwargs):
        customer_name = kwargs.get('customer_name')
        products = kwargs.get('products', [])

        if not customer_name or not products:
            return Response("Invalid data", status=400)

        # Create customer if not exists
        customer = request.env['res.partner'].search([('name', '=', customer_name)], limit=1)
        if not customer:
            customer = request.env['res.partner'].create({
                'name': customer_name
            })

        # Create POS order
        pos_order = request.env['pos.order'].create({
            'partner_id': customer.id,
        })

        # Add products to POS order line
        for product in products:
            request.env['pos.order.line'].create({
                'order_id': pos_order.id,
                'product_id': product['product_id'],
                'qty': product['quantity'],
                'price_unit': product['price']
            })

        return {'order_id': pos_order.id}
