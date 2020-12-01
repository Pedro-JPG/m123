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

    @api.multi
    def get_pricelist ( self ):
        data = {}
        data['ids'] = self._context.get('active_ids', [])
        data['model'] = self._context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read()

        return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'dtm_pricelist_report_magna.report_listado_productos',
                    'datas': data,
                }