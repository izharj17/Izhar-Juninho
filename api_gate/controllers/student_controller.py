from odoo import http
from odoo.http import request, Response
import json

class StudentListController(http.Controller):

    @http.route('/api/student_list', type='http', auth='public', methods=['GET'])
    def student_list(self, **kwargs):
        Student = request.env['op.student']
        students = Student.search([])
        student_data = []
        for student in students:
            student_data.append({
                'name ': student.first_name + student.middle_name + student.last_name
            })
        return Response(json.dumps(student_data), content_type='application/json')



class HelloWorldController(http.Controller):

    @http.route('/api/hello_world', type='http', auth='public', methods=['GET'])
    def hello_world(self, **kwargs):
        return "Hello, World!"


class StudentCountController(http.Controller):

    @http.route('/api/student_count', type='http', auth='public', methods=['GET'])
    def student_count(self, **kwargs):
        Student = request.env['op.student']
        count = Student.search_count([])
        return f"Total number of students: {count}"
    
class StudentPrestasiListController(http.Controller):

    @http.route('/api/student_prestasi_list', type='http', auth='public', methods=['GET'])
    def student_prestasi_list(self, **kwargs):
        StudentPrestasi = request.env['op.student.prestasi']
        prestasis = StudentPrestasi.search([])
        prestasi_data = []
        for prestasi in prestasis:
            prestasi_data.append({
                'nama': prestasi.nama
            })
        return Response(json.dumps(prestasi_data), content_type='application/json')