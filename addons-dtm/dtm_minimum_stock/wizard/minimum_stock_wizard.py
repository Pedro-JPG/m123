# -*- coding: utf-8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import locale
import time
import logging
# import ipdb as pdb
from openerp.exceptions import Warning


class minimum_stock_wizard(models.Model):
    _name = 'minimum.stock.wizard'
    _description = 'Imprime Informe de estado de stock'

    @api.multi
    def imprimir_repote_stock(self):
        new_context = self._context.copy()

        datas = {
            'model': 'lmo.wizard.imprimir.recibos',
            'context': new_context
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'dtm_minimum_stock.minimum_stock_report',
            'datas': datas,
        }

minimum_stock_wizard()
