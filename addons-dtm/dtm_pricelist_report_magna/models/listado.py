# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

# from openerp.osv import osv, fields

import locale
import time
from decimal import *

from openerp import api, models
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class ParticularReport(models.AbstractModel):
    _inherit = 'report.abstract_report'
    _name = 'report.dtm_pricelist_report_magna.report_listado_productos'

    def currency_fmt(self, value, fmt='%.2f'):
        locale.setlocale(locale.LC_ALL, '')
        if value == 0:
            ret = "0"
        else:
            ret = locale.format(fmt, value, grouping=True)
        return ret

    def currency_fmt_IVA(self, value, fmt='%d'):
        locale.setlocale(locale.LC_ALL, '')
        if value == 0:
            ret = "0"
        else:
            ret = locale.format(fmt, value*100, grouping=True)
        return ret

    def date_fmt(self, fecha_val):
        fecha = time.strptime(fecha_val, DEFAULT_SERVER_DATE_FORMAT)
        return "%02d/%02d/%4d" % (fecha.tm_mday, fecha.tm_mon, fecha.tm_year)

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']

        report = report_obj._get_report_from_name('dtm_pricelist_report_magna.report_listado_productos')
        wizard = self.env['pricelist.report'].browse(self._context.get('active_ids', []))

        y = self.get_pricelist(wizard)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'f_vigencia': self.date_fmt(wizard.plist_date),
            'lineas': y,
        }

        html = report_obj.render('dtm_pricelist_report_magna.report_listado_productos', docargs)
        return html


    @api.multi
    def get_pricelist(self, wizard):
        lista_qweb = []
        cat_ids = self.env['product.category'].search([])
        for categ in cat_ids:
            lista_qweb.append({'tipo': 'cat', 'name': categ.name})
            productos = self.env['product.template'].search([('categ_id', '=', categ.id)])
            for prod in productos:
                lista_qweb.append({
                    'tipo': 'prod',
                    'categ': prod.categ_id,
                    'prod_obj': prod,
                    'name': prod.name,
                    'unit': prod.list_price,
                    # 'cant': prod.uos_coeff,
                    'iva': self.currency_fmt_IVA(prod.taxes_id.amount) + "%",
                    'ext': False,
                    })

        return lista_qweb
