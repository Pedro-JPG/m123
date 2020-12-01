# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from openerp import models, fields, api, _
 
class pos_session(models.Model):
    _inherit = 'pos.session'

    def take_money_out(self, cr, uid, name, amount, session_id, context=None):
        try:
            cash_out_obj = self.pool.get('cash.box.out')
            total_amount = 0.0
            if not context:
                context = dict()
            else:
                context = context
            active_model = 'pos.session'
            active_ids = [session_id]
            if active_model == 'pos.session':
                records = self.pool.get(active_model).browse(cr, uid, active_ids)
                bank_statements = [record.cash_register_id for record in records if record.cash_register_id]
                if not bank_statements:
                    raise Warning(_('There is no cash register for this PoS Session'))
                res = cash_out_obj.create(cr, uid, {'name': name, 'amount': amount}, context)
                return cash_out_obj._run(cr, uid, [res], bank_statements, context=context)
            else:
                return {}
        except:
           return {'error':'There is no cash register for this PoS Session '}

    def put_money_in(self, cr, uid, name, amount, session_id, context=None):
        try:
            cash_out_obj = self.pool.get('cash.box.in')
            total_amount = 0.0
            if not context:
                context = dict()
            else:
                context = context
            active_model = 'pos.session'
            active_ids = [session_id]
            if active_model == 'pos.session':
                records = self.pool.get(active_model).browse(cr, uid, active_ids)
                bank_statements = [record.cash_register_id for record in records if record.cash_register_id]
                if not bank_statements:
                    raise Warning(_('There is no cash register for this PoS Session'))
                res = cash_out_obj.create(cr, uid, {'name': name, 'amount': amount}, context)
                return cash_out_obj._run(cr, uid, [res], bank_statements, context=context)
            else:
                return {}
        except:
           return {'error':'There is no cash register for this PoS Session '}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: