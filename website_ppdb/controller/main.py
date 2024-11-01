from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

class WebsitePPDB(http.Controller):

    # @http.route('/ppdb/sm', type='http', auth='public', website=True)
    # def ppdb_form(self, **kwargs):
    #     """Render the PPDB form"""
    #     return request.render('website_ppdb.ppdb_form_template_smp')


    # @http.route('/ppdb/sm', type='http', auth='public', website=True)
    # def ppdb_form(self, **kwargs):
    #     """Render the PPDB form"""

    #     admission_registers = request.env['op.admission.register'].sudo().search([('state','=','admission')])
            
    #     result = []
    #     for register in admission_registers:
    #         result.append({
    #             'id': register.id,
    #             'name': register.name,
    #             'start_date': register.start_date,
    #             'end_date': register.end_date,
    #             'course': register.course_id.name,
    #             'min_count': register.min_count,
    #             'max_count': register.max_count,
    #             'state': register.state,
    #             'academic_year': register.academic_years_id.name,
    #             'academic_term': register.academic_term_id.name,
    #             'minimum_age_criteria': register.minimum_age_criteria,
    #         })

    #     return request.render('website_ppdb.ppdb_form_template_smp', {
    #         'registers': admission_registers
    #     })

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



    # @http.route('/api/admission_register', auth='public', methods=['GET'], type='json')
    # def get_admission_register(self):
    #     try:
    #         admission_registers = request.env['op.admission.register'].sudo().search([('state','=','admission')])
            
    #         result = []
    #         for register in admission_registers:
    #             result.append({
    #                 'id': register.id,
    #                 'name': register.name,
    #                 'start_date': register.start_date,
    #                 'end_date': register.end_date,
    #                 'course': register.course_id.name,
    #                 'min_count': register.min_count,
    #                 'max_count': register.max_count,
    #                 'state': register.state,
    #                 'academic_year': register.academic_years_id.name,
    #                 'academic_term': register.academic_term_id.name,
    #                 'minimum_age_criteria': register.minimum_age_criteria,
    #             })

    #         return {'status': 200, 'data': result}

    #     except Exception as e:
    #         return {'status': 500, 'error': str(e)}



    



    
