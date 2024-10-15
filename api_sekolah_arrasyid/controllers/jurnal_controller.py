from odoo import http, _
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class FacultyJurnalController(http.Controller):

    @http.route('/api/faculty_jurnal_list', type='http', auth='public', methods=['GET'])
    def faculty_jurnal_list(self, **kwargs):
        try:
            Jurnal = request.env['op.faculty.jurnal']
            journals = Jurnal.search([])
            jurnal_data = []
            for journal in journals:
                materi_lines = []
                for line in journal.jurnal_line_ids:
                    material_name = line.material.name if line.material else ''
                    materi_lines.append({
                        'material': material_name,
                        'ketuntasan': line.ketuntasan,
                        'catatan': line.catatan,
                        
                    })
                siswa = []
                for siswa_line in journal.faculty_siswa_line_ids:
                    siswa_name = siswa_line.siswa.name if siswa_line.siswa else ''
                    siswa.append({
                        'siswa_name': siswa_name,
                        'catatan': siswa_line.catatan,
                        'taper': siswa_line.taper,
                        
                    })
                jurnal_data.append({
                    'faculty_name': journal.faculty_id.name,
                    'course_name': journal.course_id.name,
                    'date': journal.date_id.isoformat(),
                    'materi_lines': materi_lines,
                    'siswa': siswa,
                    
                })
            return Response(json.dumps(jurnal_data), content_type='application/json')

        except Exception as e:
            error_msg = _('Internal Server Error: %s') % str(e)
            _logger.error('Error occurred in faculty_jurnal_list API: %s', e)
            return Response(json.dumps({'error': error_msg}), status=500, content_type='application/json')
