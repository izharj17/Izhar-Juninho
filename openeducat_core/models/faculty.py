# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "OpenEduCat Faculty"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('First Name', size=128, translate=True)
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128, required=True)
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=1)
    last_login = fields.Datetime('Latest Connection', readonly=1,
                                 related='partner_id.user_id.login_date')
    faculty_subject_ids = fields.Many2many('op.subject', string='Subject(s)',
                                           tracking=True)
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    main_department_id = fields.Many2one(
        'op.department', 'Main Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    allowed_department_ids = fields.Many2many(
        'op.department', string='Allowed Department',
        default=lambda self:
        self.env.user.department_ids and self.env.user.department_ids.ids or False)
    # partner_id = fields.Many2one('res.partner', 'Partner',
    #                              required=True, ondelete="cascade")
    active = fields.Boolean(default=True)
    kategori = fields.Many2one('op.category', 'Kategori Guru')
    jenjang = fields.Selection([
        ('1', 'PAUD'),
        ('2', 'SD'),
        ('3', 'SM'),
    ], 'Jenjang')
    kelas_tk = fields.Boolean('Paud', size=4)
    kelas_1 = fields.Boolean('Kelas 1 SD', size=4)
    kelas_2 = fields.Boolean('Kelas 2 SD', size=4)
    kelas_3 = fields.Boolean('Kelas 3 SD', size=4)
    kelas_4 = fields.Boolean('Kelas 4 SD', size=4)
    kelas_5 = fields.Boolean('Kelas 5 SD', size=4)
    kelas_6 = fields.Boolean('Kelas 6 SD', size=4)
    kelas_7 = fields.Boolean('Kelas 7 SM', size=4)
    kelas_8 = fields.Boolean('Kelas 8 SM', size=4)
    kelas_9 = fields.Boolean('Kelas 9 SM', size=4)
    tahun_mulai = fields.Date('Awal Mengajar')
    tahun_akhir = fields.Date('Akhir Mengajar / Saat Ini')
    note = fields.Text('Deskripsi')

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name)
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Faculties'),
            'template': '/openeducat_core/static/xls/op_faculty.xls'
        }]
        
class OpFacultyJurnal(models.Model):
    _name = "op.faculty.jurnal"
    _description = "Faculty Jurnal"
    _inherit = "mail.thread"
    _rec_name = 'faculty_id'

    faculty_id = fields.Many2one('op.faculty', 'Nama Guru')
    course_id = fields.Many2one('op.course', 'Kelas')
    date_id = fields.Date('Tanggal', required=True, default=lambda self: fields.Date.today(),
        tracking=True)