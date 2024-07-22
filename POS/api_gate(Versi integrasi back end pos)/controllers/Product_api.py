from odoo import http
from odoo.http import request
import json

class ProductAPI(http.Controller):
    
    @http.route('/api/products', type='http', auth='public', methods=['GET'])
    def get_products(self):
        products = request.env['product.product'].sudo().search([('available_in_pos', '=', True)])
        product_list = []
        qty = float(request.httprequest.args.get('quantity', 1.0))
        
        for product in products:
            image_url = '/web/image/product.product/%s/image_1024' % product.id
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.list_price,
                'description': product.description or '',
                'quantity': qty,
                'image_url': request.httprequest.url_root[:-1] + image_url,
                'category': product.categ_id.name,
                'default_code': product.default_code,
            }
            product_list.append(product_data)
        return json.dumps(product_list)

    @http.route('/api/products/<int:product_id>', type='http', auth='public', methods=['GET'])
    def get_product(self, product_id):
        product = request.env['product.product'].sudo().browse(product_id)
        if not product.exists():
            return json.dumps({'error': 'Product not found'})

        image_url = '/web/image/product.product/%s/image_1024' % product.id
        qty = float(request.httprequest.args.get('quantity', 1.0))
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.list_price,
            'default_code': product.default_code,
            'quantity': qty,
            'image_url': request.httprequest.url_root[:-1] + image_url,
            'description': product.description or '',
            'category': product.categ_id.name,
        }
        return json.dumps(product_data)

    @http.route('/api/add-to-cart', type='json', auth='public', methods=['POST'])
    def add_to_cart(self):
        product_id = request.jsonrequest.get('product_id')
        quantity = int(request.jsonrequest.get('quantity', 1))

        if not product_id:
            return {'error': 'Product ID is required'}

        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart

        return {'success': True, 'message': 'Product added to cart', 'cart': cart}
    
    @http.route('/api/add-contact', type='json', auth='public', methods=['POST'])
    def add_contact(self):
        name = request.jsonrequest.get('name')
        phone = request.jsonrequest.get('phone')
        
        if not name or not phone:
            return {'error': 'Name and phone number are required'}
        
        contact = request.env['res.partner'].sudo().create({
            'name': name,
            'phone': phone,
        })
        
        return {
            'success': True,
            'message': 'Contact added successfully',
            'contact_id': contact.id
        }

   

   