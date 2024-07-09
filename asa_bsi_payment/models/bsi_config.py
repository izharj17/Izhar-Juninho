# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools
import requests
from odoo.exceptions import UserError, Warning
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime

        
class BsiConfig(models.Model):
    _name = 'bsi.conf'
    _description = "Konfigurasi Account BSI"
    _rec_name ="customer_key"
    
    customer_key    = fields.Char(string="Customer Key")
    customer_secret = fields.Char(string="Customer Secret")
    user_name       = fields.Char(string="User Name")
    password        = fields.Char(string="Password")
    base_url        = fields.Char(string="Base URL")
    auth_url        = fields.Char(string="Authorization URL")
    token           = fields.Char("Token")
    

    def get_token(self):
        for rec in self:
            consumer_key = self.customer_key
            consumer_secret = self.customer_secret
            username = self.user_name
            password = self.password

            payload = {
                'grant_type': 'password',
                'client_id': consumer_key,
                'client_secret': consumer_secret,
                'username': username,
                'password': password
            }
             
            r = requests.post(self.auth_url, 
                headers={"Content-Type":"application/x-www-form-urlencoded"},
                data=payload)

            resultreq = r.json()
            token = resultreq.get('access_token')
            token_type = resultreq.get('token_type')
            token_complete = token_type + " " + token
            print ("====token", token)
            rec.write({'token':token})
        return token
                
            
        
        

        

    
    
    