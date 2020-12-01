# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
from decimal import Decimal
import openerp.addons.decimal_precision as dp
import time
#import ipdb as pdb


class account_transfer_inherit(models.Model):
    _inherit="account.transfer"

    @api.one
    def action_confirm(self):
        voucher_obj = self.env['account.voucher']
        sval = self.voucher_get()
        dval = self.voucher_get()
        sval['company_id'] = self.company_id.id
        dval['company_id'] = self.company_id.id
        sval['journal_id'] = self.src_journal_id.id
        dval['journal_id'] = self.dst_journal_id.id
        if self.period_id:
            sval['period_id'] = self.period_id.id
            dval['period_id'] = self.period_id.id
        sval['date'] = self.date
        dval['date'] = self.date
        sval['account_id'] = self.src_journal_id.default_credit_account_id.id
        dval['account_id'] = self.dst_journal_id.default_debit_account_id.id
        sval['payment_rate'] = self.src_journal_id.currency.id and self.company_id.currency_id.id <> self.src_journal_id.currency.id and self.exchange_rate or 1.0
        dval['payment_rate'] = self.dst_journal_id.currency.id and self.company_id.currency_id.id <> self.dst_journal_id.currency.id  and self.exchange_inv or 1.0
        sval['payment_rate_currency_id'] = self.dst_journal_id.currency.id or self.company_id.currency_id.id
        dval['payment_rate_currency_id'] = self.src_journal_id.currency.id or self.company_id.currency_id.id
        sval['line_ids'][0][2]['amount'] = sval['amount'] = self.src_amount
        dval['line_ids'][0][2]['amount'] = dval['amount'] = self.dst_amount
        sval['line_ids'][0][2]['type'] = 'dr'
        dval['line_ids'][0][2]['type'] = 'cr'
        sval['line_ids'][0][2]['account_id'] = self.dst_journal_id.default_debit_account_id.id
        if self.src_partner_id.id ^ self.dst_partner_id.id:
            sval['partner_id'] = self.src_have_partner and self.src_partner_id.id or self.dst_partner_id.id
        else:
            sval['partner_id'] = self.src_have_partner and self.src_partner_id.id or self.company_id.partner_id.id
            dval['partner_id'] = self.dst_have_partner and self.dst_partner_id.id or self.company_id.partner_id.id
            account_transit = self.src_journal_id.account_transit.id
            if not account_transit:
                raise exceptions.except_osv(_('User Error!'),_(u'Configure la cuenta de tránsito en el diario de origen "%s"') % self.name)
            sval['line_ids'][0][2]['account_id'] = dval['line_ids'][0][2]['account_id'] = account_transit
            voucher_obj.create(dval)
        voucher_obj.create(sval)
        self.state = 'confirm'
        return True;