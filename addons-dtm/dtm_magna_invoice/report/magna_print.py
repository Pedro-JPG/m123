# -*- coding: utf-8 -*-
import time
from openerp.report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(order, self).__init__(cr,uid,name,context=None)
        self.localcontext.update({'time': time})


report_sxw.report_sxw('report.magna_voucher','account.voucher','addons-dtm/dtm_magna_invoice/report/report_import.rml', parser=order, header=True)
