# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#     Copyright (C) 2012 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
from decimal import Decimal
import openerp.addons.decimal_precision as dp
import time

class account_transfer(models.Model):

    #no se llama desde el api, deberia funcionar asi si se corrigen las invocaciones
    def _get_balance(self, src_journal, dst_journal, company):
        src_balance = dst_balance = 0.0
        if src_journal.default_credit_account_id.id == src_journal.default_debit_account_id.id:
            if not src_journal.currency or company.currency_id.id == src_journal.currency.id:
                src_balance = src_journal.default_credit_account_id.balance
            else:
                src_balance = src_journal.default_credit_account_id.foreign_balance
        else:
            if not src_journal.currency or company.currency_id.id == src_journal.currency.id:
                src_balance = src_journal.default_debit_account_id.balance - src_journal.default_credit_account_id.balance
            else:
                src_balance = src_journal.default_debit_account_id.foreign_balance - src_journal.default_credit_account_id.foreign_balance
        if dst_journal.default_credit_account_id.id == dst_journal.default_debit_account_id.id:
            if not dst_journal.currency or company.currency_id.id == dst_journal.currency.id:
                dst_balance = dst_journal.default_credit_account_id.balance
            else:
                dst_balance = dst_journal.default_credit_account_id.foreign_balance
        else:
            if not dst_journal.currency or company.currency_id.id == dst_journal.currency.id:
                dst_balance = dst_journal.default_debit_account_id.balance - dst_journal.default_credit_account_id.balance
            else:
                dst_balance = dst_journal.default_debit_account_id.foreign_balance - dst_journal.default_credit_account_id.foreign_balance
        
        return (src_balance, dst_balance)

    #TODO VERIFICAR ESTAS DEPENDENCIAS - no estoy seguro de que sean las correctas
    @api.one
    @api.depends("src_journal_id","dst_journal_id")
    def _balance(self):
        src_balance, dst_balance = self._get_balance(self.src_journal_id,self.dst_journal_id,self.company_id)
        self.exchange = self.dst_journal_id.currency.id != self.src_journal_id.currency.id
        self.src_balance = self. src_balance
        self.dst_balance = self.dst_balance
        self.exchange_inv = (self.exchange_rate and 1.0 / self.exchange_rate or 0.0)

    #TODO VERIFICAR ESTAS DEPENDENCIAS - no estoy seguro de que sean las correctas
    @api.one
    @api.depends("voucher_ids")
    def _move_ids(self):
	ids = []
        for v in self.voucher_ids:
                ids += [(4,l.id,False) for l in v.move_ids]
	move_ids = ids

    STATE_SELECTION = [
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done'),
        ('cancel','Cancel'),
    ]

    company_id = fields.Many2one('res.company','Company', required=True, readonly=True, states={'draft':[('readonly',False)]}, default=lambda s: s.env['res.users'].browse(s.env.uid).company_id.id)
    type = fields.Selection([('transfer','Transfer')],string='Type', required=True, readonly=True, states={'draft':[('readonly',False)]}, default='transfer')
    name = fields.Char('Number', size=32, required=True, readonly=True, states={'draft':[('readonly',False)]},
			default=lambda s: s.env['ir.sequence'].get('account.transfer'))
    date = fields.Date('Date', required=True, readonly=True, states={'draft':[('readonly',False)]},
			 default=lambda *a: time.strftime('%Y-%m-%d'))
    period_id = fields.Many2one('account.period','Period', readonly=True, states={'draft':[('readonly',False)]})
    origin = fields.Char('Origin', size=128, readonly=True, states={'draft':[('readonly',False)]},help="Origin Document")
    account_analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft':[('readonly',False)]})
    voucher_ids = fields.One2many('account.voucher','transfer_id', string='Payments', readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]})
    src_journal_id = fields.Many2one('account.journal','Source Journal',required=True, domain=[('type','in',['cash','bank'])], select=True, readonly=True, states={'draft':[('readonly',False)]})
    src_partner_id = fields.Many2one('res.partner','Source Partner', select=True, readonly=True, states={'draft':[('readonly',False)]})
    src_balance = fields.Float(compute=_balance, digits_compute=dp.get_precision('Account'), string='Balance actual del origen', readonly=True, help="Include all account moves in draft and confirmed state")
    src_amount = fields.Float('Source Amount',required=True, readonly=True, states={'draft':[('readonly',False)]})
    src_have_partner = fields.Boolean(related='src_journal_id.have_partner',string='Have Partner',readonly=True)
    dst_journal_id = fields.Many2one('account.journal','Destinity Journal',required=True, domain=[('type','in',['cash','bank'])], select=True, readonly=True, states={'draft':[('readonly',False)]})
    dst_partner_id = fields.Many2one('res.partner','Destinity Partner', select=True, readonly=True, states={'draft':[('readonly',False)]})
    dst_balance = fields.Float(compute=_balance, digits_compute=dp.get_precision('Account'), string='Balance actual del destino', readonly=True, help="Include all account moves in draft and confirmed state")
    dst_amount = fields.Float('Destinity Amount',required=True, readonly=True, states={'draft':[('readonly',False)]})
    dst_have_partner = fields.Boolean(related='dst_journal_id.have_partner',string='Have Partner',readonly=True)
    exchange_rate = fields.Float('Exchange Rate', digits_compute=dp.get_precision('Exchange'), readonly=True, states={'draft':[('readonly',False)]}, default=1.0)
    exchange = fields.Boolean(compute=_balance, string='Have Exchange', readonly=True)
    exchange_inv = fields.Float(compute=_balance, string='1 / Tipo de cambio', digits_compute=dp.get_precision('Exchange'), readonly=True, default=1.0)
    adjust_move = fields.Many2one('account.move','Adjust Move', readonly=True, help="Adjust move usually by difference in the money exchange")
    move_ids = fields.One2many('account.move.line', compute=_move_ids, string="Accounting")
    state = fields.Selection(STATE_SELECTION,string='State',track_visibility='onchange',readonly=True, default='draft')

    _sql_constraints = [('name_unique','unique(company_id,name)',_('The number must be unique!'))]
    _name = 'account.transfer'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Account Cash and Bank Transfer'
    _order = 'name desc'

    def voucher_get(self):
        res = {}
        res['transfer_id'] = self.id
        res['type'] = 'transfer'
        res['company_id'] = self.company_id.id
        res['reference'] = self.name.encode('utf-8') + str(self.origin and (' - ' + self.origin.encode('utf-8')) or '')
        res['line_ids'] = [(0,0,{})]
        res['line_ids'][0][2]['account_analytic_id'] = self.account_analytic_id and self.account_analytic_id.id or 0
        res['line_ids'][0][2]['name'] = self.origin
        return res

    def unlink(self, cr, uid, ids, context=None):
        for trans in self.browse(cr, uid, ids, context=context):
            if trans.state not in ('draft'):
                raise exceptions.except_osv(_('User Error!'),_('You cannot delete a not draft transfer "%s"') % trans.name)
        return super(account_transfer, self).unlink(cr, uid, ids, context=context)

    def copy(self, cr, uid, id, defaults, context=None):
        defaults['name'] = self.pool.get('ir.sequence').get(cr, uid, 'account.transfer')
        defaults['voucher_ids'] = []
        return super(account_transfer, self).copy(cr, uid, id, defaults, context=context)

    @api.one
    @api.onchange('src_amount','dst_amount','exchange_rate')
    def onchange_amount(self):
        new_src = 0
        new_dst = 0
        new_ext_inv = self.exchange_rate and 1.0 / self.exchange_rate or 0.0
        field = self.env.context.get('field',None)
        if field == 'src_amount':
            new_src = self.src_amount
            new_dst = self.src_amount * self.exchange_rate
        elif field == 'dst_amount':
            new_src = self.exchange_rate and self.dst_amount / self.exchange_rate or 0.0
            new_dst = self.dst_amount
        elif field == 'exchange_rate':
            new_src = self.src_amount
            new_dst = self.src_amount * self.exchange_rate
        if round(new_src, abs(Decimal(str(self.src_amount)).as_tuple().exponent)) != self.src_amount:
            self.src_amount = new_src
        if round(new_dst, abs(Decimal(str(self.dst_amount)).as_tuple().exponent)) != self.dst_amount:
            self.dst_amount = new_dst
        self.exchange_inv = new_ext_inv

    @api.one
    @api.onchange('src_journal_id','dst_journal_id')
    def onchange_journal(self):
        if not(self.src_journal_id and self.dst_journal_id):
            return
        self.src_balance, self.dst_balance = self._get_balance(self.src_journal_id,self.dst_journal_id,self.src_journal_id.company_id)
        self.exchange = self.src_journal_id.currency.id != self.dst_journal_id.currency.id
        self.src_have_partner = self.src_journal_id.have_partner
        self.dst_have_partner = self.dst_journal_id.have_partner
        #self.exchange_rate = exchange_rate
        if self.exchange:
            self.exchange_rate = (self.src_journal_id.currency and self.src_journal_id.currency.rate or self.src_journal_id.company_id.currency_id.rate) and ((self.dst_journal_id.currency and self.dst_journal_id.currency.rate or self.dst_journal_id.company_id.currency_id.rate) / (self.src_journal_id.currency and self.src_journal_id.currency.rate or self.src_journal_id.company_id.currency_id.rate)) or 0.0
        else:
            self.exchange_rate = 1.0
        self.exchange_inv = self.exchange_rate and (1.0 / self.exchange_rate) or 0.0
        self.dst_amount = self.exchange_rate * self.src_amount

    @api.one
    def action_confirm(self):
        voucher_obj = self.env['account.voucher']
        sval = self.voucher_get()
        dval = sval
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
#        return True;

    @api.one
    def action_done(self):
        voucher_obj = self.env['account.voucher']
        move_obj = self.env['account.move']
        paid_amount = []
        for voucher in self.voucher_ids:
            if voucher.state == 'draft':
                voucher.proforma_voucher()
            sign = (voucher.journal_id.id == self.src_journal_id.id) and 1 or -1
            paid_amount.append(sign * voucher._paid_amount_in_company_currency('', '')[voucher.id])
            #paid_amount.append(sign * voucher.paid_amount_in_company_currency)
        sum_amount = sum(paid_amount)
        if len(paid_amount) > 1 and sum_amount != 0.0:
            #context['company_id'] = trans.company_id.id
            periods = self.env['account.period'].find()
            period_id = self.period_id or (periods and periods[0] or False)
            move = {}
            move['journal_id'] = self.dst_journal_id.id
            move['company_id'] = self.company_id.id
            move['period_id'] = period_id.id
            move['ref'] = self.name + str(self.origin and (' - ' + self.origin) or '')
            move['date'] = self.date
            move['line_id'] = [(0,0,{}),(0,0,{})]
            move['line_id'][0][2]['name'] = self.name
            move['line_id'][1][2]['name'] = self.name
            if sum_amount > 0:
                move['line_id'][0][2]['account_id'] = self.dst_journal_id.default_debit_account_id.id
                move['line_id'][1][2]['account_id'] = self.src_journal_id.account_transit.id #self.company_id.income_currency_exchange_account_id.id
                move['line_id'][0][2]['debit'] = sum_amount
                move['line_id'][1][2]['credit'] = sum_amount
            else:
                move['line_id'][0][2]['account_id'] = self.dst_journal_id.default_credit_account_id.id
                move['line_id'][1][2]['account_id'] = self.src_journal_id.account_transit.id #self.company_id.expense_currency_exchange_account_id.id
                move['line_id'][1][2]['debit'] = -1 * sum_amount
                move['line_id'][0][2]['credit'] = -1 * sum_amount
            move_id = move_obj.create(move)
            self.write({'adjust_move':move_id.id})
        return self.write({'state':'done'})

    @api.one
    def action_cancel(self):
        voucher_obj = self.env['account.voucher']
        move_obj = self.env['account.move']
        for voucher in self.voucher_ids:
            voucher.unlink()
        if self.adjust_move:
            self.adjust_move.unlink()
        return self.write({'state':'cancel'})

    @api.one
    def action_draft(self):
        self.write({'state':'draft'})
#        wf_service = netsvc.LocalService("workflow")
#        for trans_id in ids:
#            wf_service.trg_delete(uid, 'account.transfer', trans_id, cr)
#            wf_service.trg_create(uid, 'account.transfer', trans_id, cr)
        return True

account_transfer()
