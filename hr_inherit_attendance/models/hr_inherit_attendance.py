import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions, _, SUPERUSER_ID

class HrInheritAttendance(models.Model):
    _inherit = "hr.attendance"

    status_kehadiran = fields.Selection([
        ('ot', 'Tepat Waktu'),
        ('tlb', 'Terlambat'),
        ('skt', 'Sakit'),
        ('i', 'Ijin')
    ], string='Status', compute='_compute_status_kehadiran', store=True)
    
    long_position = fields.Char('Long Position')
    lat_position = fields.Char('Lat Position')
    latetime = fields.Float('Late Time (minutes)', compute='_compute_status_kehadiran', store=True)

    @api.depends('check_in', 'check_out')
    def _compute_status_kehadiran(self):
        for record in self:
            current_time = datetime.now() + timedelta(hours=7)

            standard_check_in_time = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
            
            if standard_check_in_time - timedelta(minutes=15) <= current_time <= standard_check_in_time + timedelta(minutes=15):
                record.status_kehadiran = 'ot'  # On time
                record.latetime = 0.0  # No late time if on time
            else:
                record.status_kehadiran = 'tlb'  # Terlambat
                
                # Calculate late time in minutes
                if current_time > standard_check_in_time:
                    late_duration = current_time - standard_check_in_time
                    record.latetime = late_duration.total_seconds() / 60.0
                else:
                    record.latetime = 0.0  # In case the current time is earlier, although this shouldn't happen


class HrEmployeeBaseInherit(models.AbstractModel):
    _inherit = "hr.employee.base"

    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now() - timedelta(hours=7)

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            attendance = self.env['hr.attendance'].create(vals)
            attendance._compute_status_kehadiran()  # Trigger status computation
            return attendance
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if attendance:
            attendance.check_out = action_date
            attendance._compute_status_kehadiran()  # Trigger status computation
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        return attendance
    
    def _compute_hours_last_month(self):
        now = fields.Datetime.now() - timedelta(hours=7)
        now_utc = pytz.utc.localize(now)
        for employee in self:
            tz = pytz.timezone(employee.tz or 'UTC')
            now_tz = now_utc.astimezone(tz)
            start_tz = now_tz + relativedelta(months=-1, day=1, hour=0, minute=0, second=0, microsecond=0)
            start_naive = start_tz.astimezone(pytz.utc).replace(tzinfo=None)
            end_tz = now_tz + relativedelta(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_naive = end_tz.astimezone(pytz.utc).replace(tzinfo=None)

            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                '&',
                ('check_in', '<=', end_naive),
                ('check_out', '>=', start_naive),
            ])

            hours = 0
            for attendance in attendances:
                check_in = max(attendance.check_in, start_naive)
                check_out = min(attendance.check_out, end_naive)
                hours += (check_out - check_in).total_seconds() / 3600.0

            employee.hours_last_month = round(hours, 2)
            employee.hours_last_month_display = "%g" % employee.hours_last_month
            
        
    def _compute_hours_today(self):
        now = fields.Datetime.now() - timedelta(hours=7)
        now_utc = pytz.utc.localize(now)
        for employee in self:
            # start of day in the employee's timezone might be the previous day in utc
            tz = pytz.timezone(employee.tz)
            now_tz = now_utc.astimezone(tz)
            start_tz = now_tz + relativedelta(hour=0, minute=0)  # day start in the employee's timezone
            start_naive = start_tz.astimezone(pytz.utc).replace(tzinfo=None)

            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('check_in', '<=', now),
                '|', ('check_out', '>=', start_naive), ('check_out', '=', False),
            ])

            worked_hours = 0
            for attendance in attendances:
                delta = (attendance.check_out or now) - max(attendance.check_in, start_naive)
                worked_hours += delta.total_seconds() / 3600.0
            employee.hours_today = worked_hours
    

    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now() - timedelta(hours=7)

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if attendance:
            attendance.check_out = action_date
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        return attendance
