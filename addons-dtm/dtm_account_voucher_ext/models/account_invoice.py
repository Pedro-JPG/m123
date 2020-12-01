# -*- coding: utf-8 -*-
from openerp import api, models, exceptions, fields
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import locale
import time
#import ipdb as pdb

class account_invoice(models.Model):
    _inherit = 'account.invoice'


    @api.onchange('account_id', 'partner_id')
    def change_journal(self):
        #factura de proveedor es de tipo in_invoice
        #factura de cliente es de tipo out_invoice
        print self._context['type']
        if self._context['type'] == 'out_invoice':
            if self.account_id:
                if self.account_id.currency_id:
                    self.journal_id = self.env['account.journal'].search([('is_pago_usd', '=', True),('code', '=', 'VENME')]).id
                else:
                    self.journal_id = self.env['account.journal'].search([('is_pago_usd', '=', False),('code', '=', 'VEN$')]).id

        if self._context['type'] == 'in_invoice':
            if self.account_id:
                if self.account_id.currency_id:
                    self.journal_id = self.env['account.journal'].search([('code', '=', 'COMME')]).id
                else:
                    self.journal_id = self.env['account.journal'].search([('code', '=', 'COMPR')]).id            

        return




    @api.multi
    def invoice_validate(self):
        """
        toco el boton actualizar
        """
        self.button_reset_taxes()
        if self.account_id:
            if self.account_id.currency_id:
                self.journal_id = self.env['account.journal'].search([('is_pago_usd', '=', True),('code', '=', 'VENME')]).id
        
        return self.write({'state': 'open'})