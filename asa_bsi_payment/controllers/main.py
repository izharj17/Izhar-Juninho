# # -*- coding: utf-8 -*-
import werkzeug
import requests
import json
import pprint

from odoo import fields, http, _
from odoo.http import request, Response
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class BSIPayment(http.Controller):

    @http.route(['/payment/bsi/notification'], type='json', auth='public', csrf=False, methods=['POST'], website=True)
    def doku_notification_interface(self, **post):
        data = request.httprequest.data
        if data:
            data = json.loads(data)
            print ("============data==========", data['number'])
            invoice_ids = request.env['account.move'].sudo().search([('name','ilike',data['number'])])
            deposit = request.env['payment.deposit'].sudo().search([('name','ilike',data['number'])], limit=1)
            if invoice_ids :
                # create_payment_invoice / change state invoice to paid
                acc_payment_regis_id = request.env['account.payment.register'].with_context({
                    'active_model': 'account.move',
                    'active_ids': invoice_ids.ids,
                }).sudo().create({})        
                acc_payment_regis_id.with_context(dont_redirect_to_payments=True).action_create_payments()
            elif deposit:
                print ("==========deposit===========")
                vals =      {   
                            'deposit_id': deposit.id,
                            'date': data['date'],
                            'name': data['name'],
                            'amount': data['totalPaidAmount']
                        }

                payment_deposit = request.env['payment.deposit.line'].sudo().create(vals)
                payment_deposit.create_jurnal()
            else :
                print ("============data ndak ada==============")

        return Response('success', status=200)


