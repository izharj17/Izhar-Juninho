from odoo import _, api, fields, models

class account_voucher_group_tag(models.Model):
    _inherit = "account.voucher"

    group = fields.Many2one(
        comodel_name="master.group", string="Group"
    )

    group_tags = fields.Many2one(
        comodel_name="master.group.tags", string="Group Tags"
    )

    @api.onchange("line_ids", "group")
    def _onchange_line_ids(self):
        res = super()._onchange_line_ids()
        if self.group:
            for line in self.line_ids:
                line.group = self.group
        return res

    @api.onchange("line_ids", "group_tags")
    def _onchange_line_group_tags_ids(self):
        res = super()._onchange_line_ids()
        if self.group_tags:
            for line in self.line_ids:
                line.group_tags = self.group_tags
        return res

    @api.onchange('group', 'group_tags')
    def _onchange_group_and_group_tags(self):
        if self.move_id:  # Pastikan objek account_move sudah terkait
            # Isi field group dan group_tags di objek account_move dengan nilai dari objek account.voucher
            self.move_id.group = self.group
            self.move_id.group_tags = self.group_tags


class account_voucher_group_tag_line(models.Model):
    _inherit = "account.voucher.line"

    group = fields.Many2one(
        comodel_name="master.group", string="Group"
    )

    group_tags = fields.Many2one(
        comodel_name="master.group.tags", string="Group Tags"
    )