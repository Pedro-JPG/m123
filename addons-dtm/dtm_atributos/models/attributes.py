# -*- coding: utf-8 -*-

from openerp import models, api,fields
import time
from openerp import tools
from lxml import etree
from openerp.tools.translate import _
from datetime import datetime, date
from openerp import SUPERUSER_ID
import logging
#import ipdb as pdb

_logger = logging.getLogger(__name__)

class fix(models.TransientModel):

    _name = 'fix'
    _description = "fix invoice lines"

    archive = fields.Binary(string='Save File')

    @api.multi
    def fix_invoices(self):
        contador = 0
        ids = self._context.get('active_ids')

        #primero necesito hacerme con las facturas
        facturas = self.env['account.invoice'].search([('id','in',ids)])
        #pdb.set_trace()
        for inv in facturas:
            for line in inv.invoice_line:
                ventas = self.env['sale.order'].search([('name', '=', line.origin)])
                if ventas:
                    for ven in ventas:
                        for lineaventa in ven.order_line:
                            line.work_order_id = lineaventa.work_order_id.id