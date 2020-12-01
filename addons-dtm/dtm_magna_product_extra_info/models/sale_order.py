# -*- coding: utf_8 -*-

import unicodedata
import sys
import csv
import calendar
import time
import subprocess
import os
from os.path import basename,isfile
import string
import random
#import ipdb as pdb
import math
import base64
import datetime
import cPickle as pickle
import locale
import codecs

import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _, http
from openerp.exceptions import Warning, ValidationError
from openerp.modules import get_module_path
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition



class sale_order(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    note2 = fields.Text(string='Extra Info')

    def print_quotation(self, cr, uid, ids, context=None):
        """
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        """
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return self.pool['report'].get_action(cr, uid, ids, 'dtm_magna_product_extra_info.report_presupuesto', context=context)


sale_order()

class sale_order_line(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"


    to_print = fields.Boolean(string='¿Imprimir Monto?', default=False)

sale_order_line()
