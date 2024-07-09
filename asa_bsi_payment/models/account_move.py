# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools
import requests
from odoo.exceptions import UserError, Warning, ValidationError
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
from collections import defaultdict


class AccountMove(models.Model):
	_inherit = 'account.move'

	invoice_bsi = fields.Selection([
		('not_invoicing', 'Not Invoicing BSI'), ('invoicing_bsi', 'Invoicing BSI')],
		default='not_invoicing', string='Status Invoice BSI', copy=False,
		tracking=True)

	def send_mail_notif_invoice(self):
		for record in self :
			student = self.env['op.student'].search([('partner_id', '=', record.partner_id.id)])
			parent = student.parent_ids[0].name
			ctx = {}
			inv_line = []
			for line in record.invoice_line_ids:
				inv_line.append({'product': line.product_id.name, 'price': line.price_subtotal})


			print ("============line==========", parent.email)

			ctx['subject'] = self.partner_id.name
			ctx['email_to'] = parent.email
			ctx['email_from'] = self.env.user.email
			ctx['send_email'] = True
			ctx['va'] = student.va
			ctx['nis'] = student.nis
			ctx['kelas'] = student.category_id.name
			ctx['line_invoice'] = inv_line
			ctx['amount_total'] = self.amount_total

			template = self.env.ref('asa_bsi_payment.send_email_notif_invoice')
			template.with_context(ctx).send_mail(self.ids[0], force_send=True, raise_exception=False)


	def create_invoice_bsi(self):
		for rec in self:
			url = "/api/v2/register"
			kon = self.env['bsi.conf'].search([],limit=1)
			token = kon.get_token()
			url = kon.base_url+url
			print ("============url==============", url)
			date_str = rec.invoice_date.strftime('%Y-%m-%d')
			print ("===========token========", date_str)
			student = self.env['op.student'].search([('partner_id', '=', rec.partner_id.id)])
			if student :
				va=student.va
			else :
				va=""
			inv_line = []
			for line in rec.invoice_line_ids:
				inv_line.append({
									"description": line.name,
									"unitPrice": line.price_unit,
									"qty": line.quantity,
									"amount": line.price_subtotal
								})

			payload = {
					"date": date_str,
					"amount": rec.amount_total,
					"name": rec.partner_id.name,
					"email": rec.partner_id.email,
					"va": va,
					"attribute1": rec.payment_reference,
					"attribute2": " ",
					"openPayment": False,
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

			# self.send_mail_notif_invoice()

			rec.write({
								'invoice_bsi': 'invoicing_bsi'
						})




class OpStudent(models.Model):
	_inherit = 'op.student'

	va = fields.Char('Virtual Account') 

	def generate_va(self):
		for record in self:
			if not record.nisn:
				raise ValidationError(
					_("NISN Can't Empty....!"))

			kon = self.env['bsi.conf'].search([],limit=1)

			kode_biller = '00'
			if not kode_biller:
				raise ValidationError(
					_("Biller Code not found!"))



			record.write({
								'va': kode_biller+record.nisn
						})

class AccMoveLineInherit_group(models.Model):
    _inherit = "account.move.line"  # Do not inherit mail.thread and mail.activity.mixin again

    group = fields.Many2one(
        comodel_name="master.group", string="Group"
    )