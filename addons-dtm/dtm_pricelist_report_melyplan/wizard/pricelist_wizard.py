# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from openerp import api, models, fields, exceptions, _, http
import openerp.addons.decimal_precision as dp
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from openerp.modules import get_module_path
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception, content_disposition
import ipdb as pdb
import unicodedata
import codecs
import locale
import sys
import csv
import locale
import datetime
import calendar
import time
import subprocess
import base64
import os
from os.path import basename
import string
import random
import datetime
from decimal import Decimal
from xlwt import Workbook, Style, easyxf
from operator import itemgetter


class pricelist_report(models.TransientModel):
    _name = 'pricelist.report'

    plist_date = fields.Date(u'Fecha de Vigencia')
    plist_tarifa = fields.Many2one('product.pricelist', string="Tarifa de venta", domain=[("type", "=", "sale")])
    plist_tcambio = fields.Integer(u'Tipo de cambio')
    plist_tcambio_onch = fields.Boolean('tipo de cambio help', default=False)
    # plist_file = fields.Binary('temp')
    # plist_filename = fields.Char('temp2')

    @api.onchange('plist_tarifa')
    def _get_tcambio(self):
        if self.plist_tarifa:
            if self.plist_tarifa.currency_id.name != 'UYU':
                self.plist_tcambio_onch = True
            else:
                self.plist_tcambio_onch = False

    @api.multi
    def get_pricelist ( self ):
        # report_obj = self.env['report']
        #
        # report = report_obj._get_report_from_name('dtm_pricelist_report_melyplan.report_listado_productos')
        # # wizard = self.env['pricelist.report'].browse(self._context.get('active_ids', []))
        #
        # # y = self.get_pricelist(wizard)
        #
        # docargs = {
        #     'doc_ids': self._ids,
        #     'doc_model': report.model,
        #     'docs': self,
        #     # 'f_vigencia': self.date_fmt(wizard.plist_date),
        #
        # }
        #
        # # pdb.set_trace()
        # html = report_obj.render('dtm_pricelist_report_melyplan.report_listado_productos', docargs)
        # self.plist_filename = 'plist_report.html'
        # self.plist_file = html.encode('base64')
        # return {
        #     'context': self.env.context,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'pricelist.report',
        #     'res_id': self.id,
        #     'view_id': False,
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        # }






        data = {}
        data['ids'] = self._context.get('active_ids', [])
        data['model'] = self._context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read()

        return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'dtm_pricelist_report_melyplan.report_listado_productos',
                    'datas': data,
                }