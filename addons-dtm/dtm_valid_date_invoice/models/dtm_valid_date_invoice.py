# -*- coding: utf-8 -*-
from openerp import models, api,fields
import time
from openerp import tools
from lxml import etree
from openerp.tools.translate import _
from datetime import datetime, date
from openerp import SUPERUSER_ID
import logging
import ipdb as pdb
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)
from openerp.exceptions import Warning

class dtm_valid_date_invoice(models.Model):
   _inherit='account.invoice'

   @api.constrains('date_invoice')
   def _validate_date_invoice(self):
      if self.date_invoice:
         fecha_hoy=datetime.now().strftime('%Y-%m-%d')
         if self.date_invoice > fecha_hoy:
            raise Warning(u'La fecha de la factura debe ser menor o igual a la fecha de hoy')
