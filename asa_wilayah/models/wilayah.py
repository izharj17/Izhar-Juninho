# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


from odoo.addons import decimal_precision as dp

from werkzeug.urls import url_encode

class MasterRegion(models.Model):
    _name = "master.region"
    _description = "Master Region"
    _order = 'id desc'

    name = fields.Char('Region', required=True, copy=False, index=True, default=lambda self: _('New'))

class Provinsi(models.Model):
    _name = "wilayah.provinsi"
    _description = "Provinsi"
    _order = 'id desc'


    name = fields.Char(string='Provinsi', required=True, copy=False, index=True, default=lambda self: _('New'))
    region_id = fields.Many2one('master.region', string='Region')

class KabKota(models.Model):
    _name = "wilayah.kabkota"
    _description = "Kabupaten Kota"
    _order = 'id desc'


    name = fields.Char(string='Kabupaten/Kota', required=True, copy=False, index=True, default=lambda self: _('New'))
    provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')

class Kecamatan(models.Model):
    _name = "wilayah.kecamatan"
    _description = "Kecamatan"
    _order = 'id desc'


    name = fields.Char(string='Kecamatan', required=True, copy=False, index=True, default=lambda self: _('New'))
    kabkota_id = fields.Many2one('wilayah.kabkota', string='Kabupaten/Kota')

class Kelurahan(models.Model):
    _name = "wilayah.kelurahan"
    _description = "Kelurahan"
    _order = 'id desc'


    name = fields.Char(string='Kelurahan', required=True, copy=False, index=True, default=lambda self: _('New'))
    kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan')
    kodepos = fields.Char(string='Kodepos')    

