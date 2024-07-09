# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
from odoo.addons import decimal_precision as dp
import requests


class PaymentDeposit(models.Model):
	_name = "payment.deposit"
	_description = "Payment Deposit"
	_order = 'id desc'


	name = fields.Char(copy=False, default='New', required=True, readonly=True)
	state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('done', 'Done')], readonly=True, default='draft', copy=False, string="Status")
	date = fields.Date(string='Date', default=fields.Date.context_today, required=True, copy=False)
	communication = fields.Char(string='Memo')
	journal_id = fields.Many2one('account.journal', string='Deposit Journal', required=True, domain=[('type', 'in', ('bank', 'cash'))])
	deposit_line = fields.One2many('payment.deposit.line', 'deposit_id', string='Deposit Line')
	partner_id = fields.Many2one('res.partner', string='Partner')
	move_line_count = fields.Integer(compute="_get_move_line_count")

	def create_invoice_bsi(self):
		for rec in self:
			url = "/api/v2/register"
			kon = self.env['bsi.conf'].search([],limit=1)
			token = kon.get_token()
			url = kon.base_url+url
			print ("============url==============", url)
			date_str = rec.date.strftime('%Y-%m-%d')
			print ("===========token========", date_str)
			student = self.env['op.student'].search([('partner_id', '=', rec.partner_id.id)])
			if student :
				va=student.va
			else :
				va=""
			# inv_line = []
			# for line in rec.invoice_line_ids:
			# 	inv_line.append({
			# 						"description": line.name,
			# 						"unitPrice": line.price_unit,
			# 						"qty": line.quantity,
			# 						"amount": line.price_subtotal
			# 					})

			inv_line = [({
									"description": 'Deposit',
									"unitPrice": 0,
									"qty": 1,
									"amount": 0
								})]

			payload = {
					"date": date_str,
					"amount": 0,
					"name": rec.partner_id.name,
					"email": rec.partner_id.email,
					"va": va,
					"attribute1": rec.communication,
					"attribute2": " ",
					"openPayment": True,
					"number":rec.name,
					"items": inv_line,
					"attributes": []
				}

			print ("===========payload==========", payload)

				
			headers = {

				  'Authorization': 'Bearer '+token
				}

			print ("============header=============", headers)

			response = requests.post(url, json=payload, headers=headers)

			print (response.content)



	@api.depends('deposit_line')
	def _get_move_line_count(self):
		for statement in self:
			statement.move_line_count = len(statement.deposit_line)

	def unlink(self):
		for rec in self :
			if rec.state != 'draft' :
				raise ValidationError(_(f'Can not delete Deposit {rec.name}, state is not draft.'))
		return super(PaymentDeposit, self).unlink()

			
	def action_confirm(self):
		for rec in self:
			rec.create_invoice_bsi()
			rec.write({
				'state': 'confirm',
			})

	def action_done(self):
		for rec in self:
			rec.write({
				'state': 'done',
			})


	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('payment.deposit')
		res = super(PaymentDeposit, self).create(vals)
		return res


	def button_journal_entries(self):
		return {
			'name': _('Journal Entries'),
			'view_mode': 'tree,form',
			'res_model': 'account.move',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in', self.deposit_line.move_id.ids)],
			'context': {
				'journal_id': self.journal_id.id,
			}
		}

class PaymentProposalLine(models.Model):
	_name = "payment.deposit.line"
	_description = "Payment Proposal Line"


	deposit_id = fields.Many2one('payment.deposit', string='Payment Deposit', ondelete='cascade', copy=False)
	date       = fields.Date(string='Date', default=fields.Date.context_today, required=True, copy=False)
	name 	   = fields.Char(string='Label')
	amount 	   = fields.Float('Amount', digits=dp.get_precision('Product Price'), required=True)
	move_id	   = fields.Many2one('account.move', string='Account Move')

	def create_jurnal(self):
		for rec in self :
			debit_account = rec.deposit_id.journal_id.payment_debit_account_id.id
			credit_account = rec.deposit_id.partner_id.property_account_receivable_id.id
			amount = rec.amount

			debit_vals = {
							'name': 'Deposit',
							'partner_id': rec.deposit_id.partner_id.id,
							'debit': abs(amount),
							'credit': 0.0,
							'account_id': debit_account

							}
			credit_vals = {
								'name': 'Deposit',
								'partner_id': rec.deposit_id.partner_id.id,
								'debit': 0.0,
								'credit': abs(amount),
								'account_id': credit_account
							}

			vals =      {   
							'journal_id': rec.deposit_id.journal_id.id,
							'date': date.today(),
							'state': 'draft',
							'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
						}

			move = self.env['account.move'].create(vals)
			move.action_post()
			rec.move_id = move.id


				
