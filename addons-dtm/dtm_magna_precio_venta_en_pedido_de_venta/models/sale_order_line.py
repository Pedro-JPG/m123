# -*- coding: utf_8 -*-
from openerp.osv import fields, osv
import logging
_logger = logging.getLogger(__name__)


class sale_order_line_7(osv.osv):
    _inherit = "sale.order.line"

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False,
                          flag=False, context=None):
        dic_return = super(sale_order_line_7, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, qty_uos,
                                                                    uos, name, partner_id, lang, update_tax, date_order,
                                                                    packaging, fiscal_position, flag, context=context)

        pricelist = self.pool.get('product.pricelist').browse(cr, uid, pricelist)
        pricelist_moneda = pricelist.currency_id
        conversion = pricelist_moneda.rate_silent

        producto = self.pool.get('product.product').browse(cr, uid, product)

        if producto.list_price_type == u'manual':
            if pricelist_moneda.name == u'UYU':
                precio = producto.list_price
            else:
                precio = producto.list_price * conversion
        else:
            if pricelist_moneda.name == u'UYU':
                precio = producto.computed_list_price
            else:
                precio = producto.other_currency_list_price

        dic_return['value']['price_unit'] = precio
        return dic_return


sale_order_line_7()
