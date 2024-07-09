# from odoo import api, fields, models
#
#
# class account_payment_aa(models.Model):
#     _inherit = "account.payment"
#
#     analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', store=True)
#     effective_date = fields.Date('Effective Date',
#                                  help='Effective date of PDC', copy=False,
#                                  default=False)
#     bank_reference = fields.Char(copy=False)
#     cheque_reference = fields.Char(copy=False)
#
#     @api.model
#     def create(self, vals):
#         payment = super(account_payment_aa, self).create(vals)
#         if payment.analytic_account_id and payment.line_ids:
#             for line in payment.line_ids:
#                 line.update({'analytic_account_id': payment.analytic_account_id.id})
#         return payment
#
#     def write(self, vals):
#         result = super(account_payment_aa, self).write(vals)
#         if 'analytic_account_id' in vals and self.line_ids:
#             for line in self.line_ids:
#                 line.update({'analytic_account_id': vals['analytic_account_id']})
#         return result
#
#     @api.onchange('analytic_account_id')
#     def update_analytic_account_id(self):
#         if self.analytic_account_id:
#             AccountMove = self.env['account.move']
#             account_move_record = AccountMove.search([], limit=1)
#             if account_move_record:
#                 self.analytic_account_id = account_move_record.analytic_account_id.id
#
#
#     @api.onchange('line_ids')
#     def _onchange_line_ids(self):
#         res = super()._onchange_line_ids()
#         if self.analytic_account_id:
#             for line in self.line_ids:
#                 line.analytic_account_id = self.analytic_account_id
#         return res
#
#     # @api.depends("journal_id")
#     # def _compute_operating_unit_id(self):
#     #     for payment in self:
#     #         if payment.journal_id:
#     #             payment.operating_unit_id = payment.journal_id.operating_unit_id
#     #
#     # operating_unit_id = fields.Many2one(
#     #     comodel_name="operating.unit",
#     #     domain="[('user_ids', '=', uid)]",
#     #     compute="_compute_operating_unit_id",
#     #     store=True,
#     # )
#
#
#     # def _prepare_move_line_default_aa_vals(self, write_off_line_vals=None):
#     #     res = super()._prepare_move_line_default_aa_vals(write_off_line_vals)
#     #     for line in res:
#     #         line["analytic_account_id"] = self.analytic_account_id.id
#     #     invoices = self.env["account.move"].browse(self._context.get("active_ids"))
#     #     invoices_ou = invoices.analytic_account_id
#     #     if invoices and len(invoices_ou) == 1 and invoices_ou != self.analytic_account_id:
#     #         destination_account_id = self.destination_account_id.id
#     #         for line in res:
#     #             if line["account_id"] == destination_account_id:
#     #                 line["analytic_account_id"] = invoices_ou.id
#     #     return res