from odoo import http
from odoo.http import request
from odoo.addons.report.controllers.main import ReportController

class CustomReportController(ReportController):

    @http.route(['/custom/report/preview/<int:report_id>'], type='http', auth='user')
    def custom_report_preview(self, report_id, **post):
        report = request.env['raport.siswa.sts'].browse(report_id)
        pdf, _ = report.with_context().render_qweb_pdf()
        return http.request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'inline; filename=report.pdf')
            ]
        )

    @http.route(['/custom/report/download/<int:report_id>'], type='http', auth='user')
    def custom_report_download(self, report_id, **post):
        report = request.env['raport.siswa.sts'].browse(report_id)
        pdf, _ = report.with_context().render_qweb_pdf()
        return http.request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'attachment; filename=report.pdf')
            ]
        )
