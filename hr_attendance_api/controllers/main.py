# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request


class HrAttendanceApi(http.Controller):
    
    
    #By Employee Name
    @http.route('/api/check_in_out', type='json', auth='user')
    def check_in_out_employee(self, employee_name=None):
        """ API endpoint to check in or check out an employee by name. """
        if not employee_name not in ['check_in', 'check_out']:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by name
        employee = request.env['hr.employee'].sudo().search([('name', '=', employee_name)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Perform check-in or check-out based on action parameter
        try:
            modified_attendance = employee._attendance_action_change()

            # Additional information to return upon successful action
            last_checked_in_out = employee.last_attendance_id and (
                employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
            return {
                'employee_name': employee.name,
                'hours_today': employee.hours_today,
                
                'attendance': modified_attendance.read()[0]
            }
        except Exception as e:
            return {'error': str(e)}


    # By User ID
    @http.route('/api/check_in_out_by_user_id', type='json', auth='user')
    def check_in_out_employee_by_user_id(self, user_id=None):
        """ API endpoint to check in or check out an employee by employee.user_id. """
        if not user_id:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by user_id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', int(user_id))], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Perform check-in or check-out based on action parameter
        try:
            modified_attendance = employee.with_user(employee.user_id)._attendance_action_change()

            # Additional information to return upon successful action
            last_checked_in_out = employee.last_attendance_id and (
                employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
            return {
                'employee_name': employee.name,
                'hours_today': employee.hours_today,
                'last_checked_in_out': last_checked_in_out,
                'attendance': modified_attendance.read()[0]
            }
        except Exception as e:
            return {'error': str(e)}
        
        
    #By Barcode
    @http.route('/api/check_in_out_by_barcode', type='json', auth='user')
    def check_in_out_employee_by_barcode(self, barcode=None):
        """ API endpoint to check in or check out an employee by barcode. """
        if not barcode:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by barcode
        employee = request.env['hr.employee'].sudo().search([('barcode', '=', barcode)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Perform check-in or check-out based on action parameter
        try:
            modified_attendance = employee._attendance_action_change()

            # Additional information to return upon successful action
            last_checked_in_out = employee.last_attendance_id and (
                employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
            return {
                'employee_name': employee.name,
                'hours_today': employee.hours_today,
                
                'attendance': modified_attendance.read()[0]
            }
        except Exception as e:
            return {'error': str(e)}