from odoo import models, fields, api

class KpiSupervisi(models.Model):
    _name = 'kpi.supervisi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Management"
    _rec_name = 'guru_id'

    guru_id = fields.Many2one('hr.employee', 'Guru')
    department_id = fields.Many2one('hr.department', 'Bagian', related='guru_id.department_id')
    tahun_kpi = fields.Many2one('op.academic.year','Tahun Ajaran')
    semester_kpi = fields.Many2one('op.academic.term','Semester')
    nama_sekolah = fields.Many2one('res.company', 'Sekolah')
    nilai_akhir = fields.Float('Nilai Akhir Supervisi')
    kpi_ids_rekap = fields.One2many('kpi.supervisi.rekap', 'kpi_supervisi_rekap', string='KPI Rekap')
    kpi_ids_rekap_1 = fields.One2many('kpi.supervisi.rekap.1', 'kpi_supervisi_rekap_1', string='KPI Rekap 1')
    kpi_ids_rekap_2 = fields.One2many('kpi.supervisi.rekap.2', 'kpi_supervisi_rekap_2', string='KPI Rekap 2')
    kpi_ids_rekap_3 = fields.One2many('kpi.supervisi.rekap.3', 'kpi_supervisi_rekap_3', string='KPI Rekap 3')
    kpi_ids_1 = fields.One2many('kpi.supervisi.line.1', 'kpi_supervisi_line_1', string='KPI Line 1')
    kpi_ids_2 = fields.One2many('kpi.supervisi.line.2', 'kpi_supervisi_line_2', string='KPI Line 2')
    kpi_ids_3 = fields.One2many('kpi.supervisi.line.3', 'kpi_supervisi_line_3', string='KPI Line 3')
    kpi_ids_4 = fields.One2many('kpi.supervisi.line.4', 'kpi_supervisi_line_4', string='KPI Line 4')
    kpi_ids_5 = fields.One2many('kpi.supervisi.line.5', 'kpi_supervisi_line_5', string='KPI Line 5')
    kpi_ids_6 = fields.One2many('kpi.supervisi.line.6', 'kpi_supervisi_line_6', string='KPI Line 6')
    kpi_ids_7 = fields.One2many('kpi.supervisi.line.7', 'kpi_supervisi_line_7', string='KPI Line 7')
    kpi_ids_8 = fields.One2many('kpi.supervisi.line.8', 'kpi_supervisi_line_8', string='KPI Line 8')
    kpi_ids_9 = fields.One2many('kpi.supervisi.line.9', 'kpi_supervisi_line_9', string='KPI Line 9')
    kpi_ids_10 = fields.One2many('kpi.supervisi.line.10', 'kpi_supervisi_line_10', string='KPI Line 10')
    kpi_ids_11 = fields.One2many('kpi.supervisi.line.11', 'kpi_supervisi_line_11', string='KPI Line 11')
    kpi_ids_12 = fields.One2many('kpi.supervisi.line.12', 'kpi_supervisi_line_12', string='KPI Line 12')
    kpi_ids_13 = fields.One2many('kpi.supervisi.line.13', 'kpi_supervisi_line_13', string='KPI Line 13')
    kpi_ids_14 = fields.One2many('kpi.supervisi.line.14', 'kpi_supervisi_line_14', string='KPI Line 14')
    
class KpiSupervisirekap(models.Model):
    _name = 'kpi.supervisi.rekap'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Rekap"

    kpi_supervisi_rekap = fields.Many2one('kpi.supervisi', string='Survey')
    question_rekap = fields.Text('Indikator', size=5)
    skor_rekap = fields.Float('Skor', size=4)
    
class KpiSupervisirekap(models.Model):
    _name = 'kpi.supervisi.rekap.1'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Rekap 1"

    kpi_supervisi_rekap_1 = fields.Many2one('kpi.supervisi', string='Survey')
    question_rekap_1 = fields.Text('Indikator', size=5)
    skor_rekap_1 = fields.Float('Skor', size=4)
    
class KpiSupervisirekap(models.Model):
    _name = 'kpi.supervisi.rekap.2'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Rekap 2"

    kpi_supervisi_rekap_2 = fields.Many2one('kpi.supervisi', string='Survey')
    question_rekap_2 = fields.Text('Indikator', size=5)
    skor_rekap_2 = fields.Float('Skor', size=4)
    
class KpiSupervisirekap(models.Model):
    _name = 'kpi.supervisi.rekap.3'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Rekap 3"

    kpi_supervisi_rekap_3 = fields.Many2one('kpi.supervisi', string='Survey')
    question_rekap_3 = fields.Text('Indikator', size=5)
    skor_rekap_3 = fields.Float('Skor', size=4)
    
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.1'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 1"

    kpi_supervisi_line_1 = fields.Many2one('kpi.supervisi', string='Survey')
    question_1 = fields.Text('Indikator', size=8)
    skor_1 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_2 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_3 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.2'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 2"

    kpi_supervisi_line_2 = fields.Many2one('kpi.supervisi', string='Survey')
    question_2 = fields.Text('Indikator', size=8)
    skor_4 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_5 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_6 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.3'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 3"

    kpi_supervisi_line_3 = fields.Many2one('kpi.supervisi', string='Survey')
    question_3 = fields.Text('Indikator', size=8)
    skor_7 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_8 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_9 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.4'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 4"

    kpi_supervisi_line_4 = fields.Many2one('kpi.supervisi', string='Survey')
    question_4 = fields.Text('Indikator', size=8)
    skor_10 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_11 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_12 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.5'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 5"

    kpi_supervisi_line_5 = fields.Many2one('kpi.supervisi', string='Survey')
    question_5 = fields.Text('Indikator', size=8)
    skor_13 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_14 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_15 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.6'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 6"

    kpi_supervisi_line_6 = fields.Many2one('kpi.supervisi', string='Survey')
    question_6 = fields.Text('Indikator', size=8)
    skor_16 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_17 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_18 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.7'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 7"

    kpi_supervisi_line_7 = fields.Many2one('kpi.supervisi', string='Survey')
    question_7 = fields.Text('Indikator', size=8)
    skor_19 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_20 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_21 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.8'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 8"

    kpi_supervisi_line_8 = fields.Many2one('kpi.supervisi', string='Survey')
    question_8 = fields.Text('Indikator', size=8)
    skor_22 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_23 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_24 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.9'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 9"

    kpi_supervisi_line_9 = fields.Many2one('kpi.supervisi', string='Survey')
    question_9 = fields.Text('Indikator', size=8)
    skor_25 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_26 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_27 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.10'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 10"

    kpi_supervisi_line_10 = fields.Many2one('kpi.supervisi', string='Survey')
    question_10 = fields.Text('Indikator', size=8)
    skor_28 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_29 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_30 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.11'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 11"

    kpi_supervisi_line_11 = fields.Many2one('kpi.supervisi', string='Survey')
    question_11 = fields.Text('Indikator', size=8)
    skor_31 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_32 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_33 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.12'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 12"

    kpi_supervisi_line_12 = fields.Many2one('kpi.supervisi', string='Survey')
    question_12 = fields.Text('Indikator', size=8)
    skor_34 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_35 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_36 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.13'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 13"

    kpi_supervisi_line_13 = fields.Many2one('kpi.supervisi', string='Survey')
    question_13 = fields.Text('Indikator', size=8)
    skor_37 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_38 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_39 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)
    
class KpiSupervisiline(models.Model):
    _name = 'kpi.supervisi.line.14'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "KPI Line 14"

    kpi_supervisi_line_14 = fields.Many2one('kpi.supervisi', string='Survey')
    question_14 = fields.Text('Indikator', size=8)
    skor_40 = fields.Float('Skor (Tidak Terpenuhi)', size=4)
    skor_41 = fields.Float('Skor (Sebagian Terpenuhi)', size=4)
    skor_42 = fields.Float('Skor (Seluruhnya Terpenuhi)', size=4)