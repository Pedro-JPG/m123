# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class account_bank_statement(osv.osv):
	
    _name = "account.bank.statement"
    _inherit = "account.bank.statement"    
    _columns = { 
	
        'cash_control': fields.related('journal_id', 'cash_control', type='boolean', relation='account.journal', help='If you want the journal should be control at opening/closing, check this option', string='Cash Control' ),
		
    }
	
    def balance_check(self, cr, uid, st_id, journal_type='bank', context=None):
        st = self.browse(cr, uid, st_id, context=context)       
        if self.browse(cr, uid, st_id, context=context).cash_control:
            if not ((abs((st.balance_end or 0.0) - st.balance_end_real) < 0.0001) or (abs((st.balance_end or 0.0) - st.balance_end_real) < 0.0001)):
                raise osv.except_osv(_('Error!'),
                    _('The statement balance is incorrect !\nThe expected balance (%.2f) is different than the computed one. (%.2f)') % (st.balance_end_real, st.balance_end))
        else:
            pass			
        return True  
		
account_bank_statement()  
