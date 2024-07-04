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