# -*- coding: utf_8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import locale
import time
import logging
import ipdb as pdb
from openerp.exceptions import Warning
import collections
_logger = logging.getLogger(__name__)

class account_voucher(models.Model):
    _inherit = 'account.voucher'
    _description = 'Accounting Voucher, extension'




    @api.one
    def button_setear_vacio(self):
        for line in self.line_ids:
            line.reconcile = 0
            line.amount = 0.0


    @api.multi
    def button_eleminar_no_conciliado(self):
        for line in self.line_ids:
            if not line.amount:
                self.write({'line_ids': [(3,line.id,_)],})