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
    _name = 'report.dtm_pricelist_report_melyplan.report_listado_productos'

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

        report = report_obj._get_report_from_name('dtm_pricelist_report_melyplan.report_listado_productos')
        wizard = self.env['pricelist.report'].browse(self._context.get('active_ids', []))

        y = self.get_pricelist(wizard)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'f_vigencia': self.date_fmt(wizard.plist_date),
            'lineas': y,
        }

        # pdb.set_trace()
        html = report_obj.render('dtm_pricelist_report_melyplan.report_listado_productos', docargs)
        return html
        # wizard.plist_file = html.encode('base64')
        #
        # wizard.plist_filename = 'plist_report.html'
        # wizard.plist_file = html.encode('base64')
        # return {
        #     'context': wizard.env.context,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'pricelist.report',
        #     'res_id': wizard.id,
        #     'view_id': False,
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        # }

    def get_desc(self, wizard):
        lista_desc = []
        for a in wizard.plist_tarifa.version_id:
            for b in a.items_id:
                lista_desc.append(b)
        return lista_desc

    @api.multi
    def get_pricelist(self, wizard):
        lista_qweb = []
        ldesc = self.get_desc(wizard)
        moneda = wizard.plist_tarifa.currency_id.name or False

        """
        Lista devuelta:
        []

        Diccionario categ:

        {
            tipo:"cat",
            name:"ph",
        }

        Diccionario prod:

        {
            tipo:"prod",
            name:"ph",
            cant: 100, CANT UDV
            iva:"10%",
            xcaja:1300,
            unit:13,

        }
        """
        if moneda == 'UYU':
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
                        'cant': prod.uos_coeff,
                        'iva': self.currency_fmt_IVA(prod.taxes_id.amount) + "%",
                        'ext': False,
                        # 'xcaja': prod.list_price,
                        # 'unit': prod.list_price / (prod.uos_coeff or 1),
                    })

        else:
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
                        'cant': prod.uos_coeff,
                        'iva': self.currency_fmt_IVA(prod.taxes_id.amount) + "%",
                        'ext':True,
                        # 'xcaja': prod.list_price / wizard.plist_tcambio,
                        # 'unit': (prod.list_price / prod.uos_coeff or 1) / wizard.plist_tcambio,
                    })
        for item in lista_qweb:
            if item['tipo'] == 'prod':
                for desc in ldesc:
                    if (item['prod_obj'] == desc.product_tmpl_id) or (item['categ'] == desc.categ_id) or (
                            desc.categ_id.id == False and desc.product_tmpl_id.id == False):
                        temp_desc= 1 + (desc.price_discount or 0)
                        if item['ext']:
                            if 'xcaja' not in item.keys():
                                item['xcaja'] = (item['prod_obj'].list_price / wizard.plist_tcambio) * temp_desc
                            else:
                                item['xcaja'] = float(item['xcaja']) * temp_desc
                            if 'unit' not in item.keys():
                                item['xcaja'] = ((item['prod_obj'].list_price / ( item['prod_obj'].uos_coeff or 1 ) ) / wizard.plist_tcambio) * temp_desc
                            else:
                                item['unit'] = float(item['unit']) * temp_desc
                        else:
                            if 'xcaja' not in item.keys():
                                item['xcaja'] = item['prod_obj'].list_price  * temp_desc
                            else:
                                item['xcaja'] = float(item['xcaja']) * temp_desc
                            if 'unit' not in item.keys():
                                item['unit'] = (item['prod_obj'].list_price / ( item['prod_obj'].uos_coeff or 1 ) )  * temp_desc
                            else:
                                item['unit'] = float(item['unit']) * temp_desc
                    else:
                        if item['ext']:
                            if 'xcaja' not in item.keys():
                                item['xcaja'] = (item['prod_obj'].list_price / wizard.plist_tcambio)
                            if 'unit' not in item.keys():
                                item['unit'] = ((item['prod_obj'].list_price / ( item['prod_obj'].uos_coeff or 1 ) ) / wizard.plist_tcambio)
                        else:
                            if 'xcaja' not in item.keys():
                                item['xcaja'] = item['prod_obj'].list_price
                            if 'unit' not in item.keys():
                                item['unit'] = (item['prod_obj'].list_price / ( item['prod_obj'].uos_coeff or 1 ) )
                    if desc == ldesc[-1]:
                        item['xcaja'] = self.currency_fmt(item['xcaja'])
                        item['unit'] = self.currency_fmt(item['unit'])

        return lista_qweb
