from odoo import api, models, _
from odoo.exceptions import UserError


class MassCreateInvoiceBsi(models.TransientModel):
    _name = 'mass.create.invoice.bsi'


    def create_invoice_bsi(self):
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', [])), ('state', '=', 'posted')]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        moves = self.env['account.move'].search(domain).filtered('line_ids')
        if not moves:
            raise UserError(_('There are no Invoice in the Post state.'))
        moves.create_invoice_bsi()
        return {'type': 'ir.actions.act_window_close'}

    
