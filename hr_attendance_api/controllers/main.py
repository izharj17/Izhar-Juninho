from odoo import http, exceptions, fields, _
from odoo.http import request
from datetime import datetime, timedelta

class HrAttendanceApi(http.Controller):
    
    # By Employee Name
    @http.route('/api/check_in_out', type='json', auth='user')
    def check_in_out_employee(self, employee_name=None, url=None):
        """ API endpoint to check in or check out an employee by name. """
        if not employee_name or not url:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by name
        employee = request.env['hr.employee'].sudo().search([('name', '=', employee_name)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Perform check-in or check-out action with URL
        try:
            modified_attendance = employee._attendance_action_change(url)

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
    def check_in_out_employee_by_user_id(self, user_id=None, url=None):
        """ API endpoint to check in or check out an employee by employee.user_id. """
        if not user_id or not url:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by user_id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', int(user_id))], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Perform check-in or check-out action with URL
        try:
            modified_attendance = employee.with_user(employee.user_id)._attendance_action_change(url)

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
        
    # By Barcode
    @http.route('/api/check_in_out_by_barcode', type='json', auth='user')
    def check_in_out_employee_by_barcode(self, barcode=None, url=None):
        """ API endpoint to check in or check out an employee by barcode. """
        if not barcode or not url:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by barcode
        employee = request.env['hr.employee'].sudo().search([('barcode', '=', barcode)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Perform check-in or check-out action with URL
        try:
            modified_attendance = employee._attendance_action_change(url)

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
        
    


# GET THE ATTENDANCES

    @http.route('/api/get_attendance', type='json', auth='user')
    def get_attendance_this_week(self):
        """ API endpoint to retrieve attendance records for the current week for the logged-in user. """
        
        # Get the current logged-in user
        user = request.env.user

        # Find the employee linked to the current user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Get current date and time
        now = fields.Datetime.now()

        # Calculate the start of the week
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = start_of_day - timedelta(days=start_of_day.weekday())

        # Fetch attendance records for the week
        domain = [('employee_id', '=', employee.id)]
        attendance_this_week = request.env['hr.attendance'].sudo().search(domain + [('check_in', '>=', start_of_week)])

        # Convert records to a readable format
        attendance_this_week_data = attendance_this_week.read(['check_in', 'check_out', 'status_kehadiran', 'url_checkin', 'url_checkout'])

        return {
            'employee_name': employee.name,
            'attendance_this_week': attendance_this_week_data,
        }
        
    @http.route('/api/get_attendance_qr', type='json', auth='user')
    def get_attendance_this_qr_week(self, barcode=None):
        """ API endpoint to retrieve attendance records for the current week for the employee identified by barcode. """
        if not barcode:
            return {'error': _('Invalid request parameters.')}

        # Find the employee by barcode
        employee = request.env['hr.employee'].sudo().search([('barcode', '=', barcode)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Get current date and time
        now = fields.Datetime.now()

        # Calculate the start of the week
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = start_of_day - timedelta(days=start_of_day.weekday())

        # Fetch attendance records for the week
        domain = [('employee_id', '=', employee.id)]
        attendance_this_week = request.env['hr.attendance'].sudo().search(domain + [('check_in', '>=', start_of_week)])

        # Convert records to a readable format
        attendance_this_week_data = attendance_this_week.read(['check_in', 'check_out', 'status_kehadiran', 'url_checkin', 'url_checkout'])

        return {
            'employee_name': employee.name,
            'attendance_this_week': attendance_this_week_data,
        }
        
    @http.route('/api/get_attendance_this_month', type='json', auth='user')
    def get_attendance_this_month(self):
        """ API endpoint to retrieve attendance records for the current month for the logged-in user. """
        
        # Get the current logged-in user
        user = request.env.user

        # Find the employee linked to the current user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Get current date and time
        now = fields.Datetime.now()

        # Calculate the start of the month
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the end of the month
        if now.month == 12:
            end_of_month = start_of_month.replace(year=now.year + 1, month=1)
        else:
            end_of_month = start_of_month.replace(month=now.month + 1)

        # Fetch attendance records for the month
        domain = [('employee_id', '=', employee.id)]
        attendance_this_month = request.env['hr.attendance'].sudo().search(domain + [('check_in', '>=', start_of_month), ('check_in', '<', end_of_month)])

        # Convert records to a readable format
        attendance_this_month_data = attendance_this_month.read(['check_in', 'check_out', 'status_kehadiran', 'url_checkin', 'url_checkout'])

        return {
            'employee_name': employee.name,
            'attendance_this_month': attendance_this_month_data,
        }
        
    @http.route('/api/get_attendance_this_year', type='json', auth='user')
    def get_attendance_this_year(self):
        """ API endpoint to retrieve attendance records for the current year for the logged-in user. """
        
        # Get the current logged-in user
        user = request.env.user

        # Find the employee linked to the current user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not employee:
            return {'error': _('Employee not found.')}

        # Get current date and time
        now = fields.Datetime.now()

        # Calculate the start of the year
        start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the end of the year
        end_of_year = start_of_year.replace(year=now.year + 1)

        # Fetch attendance records for the year
        domain = [('employee_id', '=', employee.id)]
        attendance_this_year = request.env['hr.attendance'].sudo().search(domain + [('check_in', '>=', start_of_year), ('check_in', '<', end_of_year)])

        # Convert records to a readable format
        attendance_this_year_data = attendance_this_year.read(['check_in', 'check_out', 'status_kehadiran', 'url_checkin', 'url_checkout'])

        return {
            'employee_name': employee.name,
            'attendance_this_year': attendance_this_year_data,
        }