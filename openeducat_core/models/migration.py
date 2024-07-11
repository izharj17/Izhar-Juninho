from datetime import date
from odoo import models, fields, api, _

class OpMigration(models.Model):
    _name = 'op.migration'
    _description = 'Student Migration'

    name = fields.Char('Migration Name', required=True)
    student_ids = fields.Many2many('op.student', string='Students', domain="[('grade', '=', old_course_id)]")
    old_course_id = fields.Many2one('op.course', 'Old Grade', required=True)
    new_course_id = fields.Many2one('op.course', 'New Grade', required=True)
    new_batch_id = fields.Many2one('op.batch', 'New Rombel', required=True)
    new_academic_year_id = fields.Many2one('op.academic.year', 'New Academic Year', required=True)
    new_academic_term_id = fields.Many2one('op.academic.term', 'New Academic Term', required=True)
    migration_date = fields.Date('Migration Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('migrated', 'Migrated'),
    ], string='State', default='draft')

    @api.onchange('old_course_id')
    def _onchange_old_course_id(self):
        domain = [('id', 'in', self.student_ids.ids)]  # Initialize with current selection

        # If old_course_id is set, filter students by course_detail_ids matching old_course_id
        if self.old_course_id:
            student_ids = self.env['op.student'].search([('course_detail_ids.course_id', '=', self.old_course_id.id)])
            domain = [('id', 'in', student_ids.ids)]

        return {'domain': {'student_ids': domain}}

    @api.model
    def migrate_students(self):
        for record in self:
            for student in record.student_ids:
                # Delete all existing course details for the student
                student.course_detail_ids.unlink()

                # Get all subjects from the selected new course
                subject_ids = [(6, 0, record.new_course_id.subject_ids.ids)]
                
                # Create a new course detail with the new grade
                self.env['op.student.course'].create({
                    'student_id': student.id,
                    'course_id': record.new_course_id.id,
                    'batch_id': record.new_batch_id.id,
                    'roll_number': student.nis,
                    'subject_ids': subject_ids,
                    'academic_years_id': record.new_academic_year_id.id,
                    'academic_term_id': record.new_academic_term_id.id,
                    'state': 'running',
                })
                
                # Update the student's grade to the new grade
                student.write({'grade': record.new_course_id.id})

            # Update state to 'Migrated' after successfully migrating students
            record.write({'state': 'migrated'})
            # Update migration date to today
            record.write({'migration_date': date.today()})

        return True

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
        
    def action_set_to_ready(self):
        self.write({'state': 'ready'})
        
    def action_done_migrated(self):
        self.migrate_students()
        return True
