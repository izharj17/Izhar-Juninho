# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class account_move_aa(models.Model):
    _inherit = "account.move"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic Account"
    )

    group = fields.Many2one(
        comodel_name="master.group", string="Group"
    )
    #
    # group_tags = fields.Many2one(
    #     comodel_name="master.group.tags", string="Group Tags"
    # )

    @api.onchange("invoice_line_ids", "analytic_account_id")
    def _onchange_invoice_line_ids(self):
        res = super()._onchange_invoice_line_ids()
        if self.analytic_account_id:
            for line in self.line_ids:
                line.analytic_account_id = self.analytic_account_id
        return res

    # @api.onchange("line_ids", "analytic_account_id")
    # def _onchange_line_ids(self):
    #     if self.analytic_account_id:
    #         for line in self.line_ids:
    #             line.analytic_account_id = self.analytic_account_id


# class AccountMoveLine(models.Model):
#     _inherit = "account.move.line"
#
#     operating_unit_id = fields.Many2one(
#         comodel_name="operating.unit", domain="[('user_ids', '=', uid)]"
#     )
#
#     @api.model_create_multi
#     def create(self, vals_list):
#         for vals in vals_list:
#             if vals.get("move_id", False):
#                 move = self.env["account.move"].browse(vals["move_id"])
#                 if move.operating_unit_id:
#                     vals["operating_unit_id"] = move.operating_unit_id.id
#         return super().create(vals_list)

# class purchase_request_product(models.Model):
#     _inherit = "purchase.request"
#
#     product_id = fields.Many2one('product.product', 'Product')

# class account_move_aa(models.Model):
#     _inherit = "purchase.request"
#
#     analytic_account_id = fields.Many2one(
#         comodel_name="account.analytic.account", string="Analytic Account"
#     )

    # @api.onchange("invoice_line_ids", "analytic_account_id")
    # def _onchange_invoice_line_ids(self):
    #     res = super()._onchange_invoice_line_ids()
    #     if self.analytic_account_id:
    #         for line in self.line_ids:
    #             line.analytic_account_id = self.analytic_account_id
    #     return res
    #
    # @api.onchange("line_ids", "analytic_account_id")
    # def _onchange_line_ids(self):
    #     if self.analytic_account_id:
    #         for line in self.line_ids:
    #             line.analytic_account_id = self.analytic_account_id

    # @api.onchange("operating_unit_id")
    # def _onchange_operating_unit(self):
    #     if self.operating_unit_id and (
    #             not self.journal_id
    #             or self.journal_id.operating_unit_id != self.operating_unit_id
    #     ):
    #         journal = self.env["account.journal"].search(
    #             [("type", "=", self.journal_id.type)]
    #         )
    #         jf = journal.filtered(
    #             lambda aj: aj.operating_unit_id == self.operating_unit_id
    #         )
    #         if not jf:
    #             self.journal_id = journal[0]
    #         else:
    #             self.journal_id = jf[0]
    #         for line in self.line_ids:
    #             line.operating_unit_id = self.operating_unit_id