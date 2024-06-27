from odoo import http
from odoo.http import request, Response
import json

class FacultyJurnalController(http.Controller):

    @http.route('/api/faculty_jurnal_list', type='http', auth='public', methods=['GET'])
    def faculty_jurnal_list(self, **kwargs):
        Jurnal = request.env['op.faculty.jurnal']
        journals = Jurnal.search([])
        jurnal_data = []
        for journal in journals:
            journal_lines = []
            for line in journal.jurnal_line_ids:
                journal_lines.append({
                    'material': line.material.name if line.material else '',
                    'ketuntasan': line.ketuntasan,
                    'catatan': line.catatan,
                    # Add more fields as needed
                })
            siswa_lines = []
            for siswa_line in journal.faculty_siswa_line_ids:
                siswa_lines.append({
                    'siswa_name': siswa_line.siswa.name if siswa_line.siswa else '',
                    'catatan': siswa_line.catatan,
                    'taper': siswa_line.taper,
                    # Add more fields as needed
                })
            jurnal_data.append({
                'faculty_name': journal.faculty_id.name,
                'course_name': journal.course_id.name,
                'date': journal.date_id,
                'journal_lines': journal_lines,
                'siswa_lines': siswa_lines,
                # Add more fields from OpFacultyJurnal model if needed
            })
        return Response(json.dumps(jurnal_data), content_type='application/json')
