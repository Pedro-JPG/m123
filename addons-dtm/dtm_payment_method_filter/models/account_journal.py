# -*- coding: utf_8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import locale
import time
import logging
# import ipdb as pdb
from openerp.exceptions import Warning
_logger = logging.getLogger(__name__)

class account_journal(models.Model):

    _inherit='account.journal'

    metodo_pago = fields.Boolean(string=u'Es metodo de pago a proveedores?', help='Selecione esta opcion si es un metodo de pago a proveedores')
    is_pago_usd = fields.Boolean(string=u'¿Es Diario de Ventas Dolares?')

account_journal()
