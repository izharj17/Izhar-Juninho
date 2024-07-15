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

from odoo import models, fields, api


class OpAttendanceSheet(models.Model):
    _name = "op.attendance.sheet"
    _inherit = ["mail.thread"]
    _description = "Attendance Sheet"
    _order = "attendance_date desc"

    name = fields.Char('Name', readonly=True, size=32)
    agenda = fields.Text('Agenda', required=True, size=256)
    register_id = fields.Many2one(
        'op.attendance.register', 'Register', required=True,
        tracking=True)
    course_id = fields.Many2one(
        'op.course', 'Grade', related='register_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Rombel', related='register_id.batch_id', store=True,
        readonly=True)
    session_id = fields.Many2one('op.session', 'Session')
    attendance_date = fields.Date(
        'Date', required=True, default=lambda self: fields.Date.today(),
        tracking=True)
    attendance_line = fields.One2many(
        'op.attendance.line', 'attendance_id', 'Attendance Line',)
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    active = fields.Boolean(default=True)

    state = fields.Selection(
        [('draft', 'Draft'), ('start', 'Attendance Start'),
         ('done', 'Attendance Taken'), ('cancel', 'Cancelled')],
        'Status', default='draft', tracking=True)

    def attendance_draft(self):
        self.state = 'draft'

    def attendance_start(self):
        self.state = 'start'

    def attendance_done(self):
        self.state = 'done'

    def attendance_cancel(self):
        self.state = 'cancel'

    _sql_constraints = [
        ('unique_register_sheet',
         'unique(register_id,session_id,attendance_date)',
         'Sheet must be unique per Register/Session.'),
    ]

    @api.onchange('register_id')
    def onchange_register_id(self):
        if self.register_id:
            # Get all students enrolled in the same course as the register
            students = self.env['op.student'].search([
                ('course_detail_ids.course_id', '=', self.register_id.course_id.id),('course_detail_ids.batch_id','=',self.register_id.batch_id.id)
            ])
            # Clear existing attendance lines and recreate for each student
            self.attendance_line = [(5, 0, 0)]  # Clear existing lines
            for student in students:
                self.attendance_line = [(0, 0, {
                    'student_id': student.id,
                    'attendance_id': self.id,
                    'present': True,  # Initialize defaults if needed
                    'excused': False,
                    'absent': False,
                    'late': False,
                    'sick': False,
                })]

    @api.model
    def create(self, vals):
        sheet = self.env['ir.sequence'].next_by_code('op.attendance.sheet')
        register = self.env['op.attendance.register'].browse(vals['register_id']).code
        vals['name'] = register + sheet
        return super(OpAttendanceSheet, self).create(vals)
