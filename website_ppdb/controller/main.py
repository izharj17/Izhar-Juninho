from odoo import http
from odoo.http import request

class WebsitePPDB(http.Controller):

    @http.route('/ppdbsm', type='http', auth='public', website=True)
    def ppdb_form(self, **kwargs):
        """Render the PPDB form"""
        return request.render('website_ppdb.ppdb_form_template_SM')
    
    @http.route('/ppdbsd', type='http', auth='public', website=True)
    def ppdb_form(self, **kwargs):
        """Render the PPDB form"""
        return request.render('website_ppdb.ppdb_form_template_SD')
    
    @http.route('/ppdb', type='http', auth='public', website=True)
    def ppdb_form(self, **kwargs):
        """Render the PPDB form"""
        return request.render('website_ppdb.ppdb_form_template_TK')

    @http.route('/ppdb/submit', type='http', auth='public', website=True, csrf=False)
    def submit_ppdb(self, **post):
        """Handle PPDB form submission"""
        # Create a new record in 'op.ppdb' model
        vals = {
            'nama_lengkap': post.get('nama_lengkap'),
            'nama_panggilan': post.get('nama_panggilan'),
            'jenis_kelamin': post.get('jenis_kelamin'),
            'nisn': post.get('nisn'),
            'nik': post.get('nik'),
            'tempat_lahir': post.get('tempat_lahir'),
            'tgl_lahir': post.get('tgl_lahir'),
            'akte': post.get('akte'),
            'agama': post.get('agama'),
        }
        request.env['op.ppdb'].sudo().create(vals)
        return request.render('website_ppdb.ppdb_success_template')