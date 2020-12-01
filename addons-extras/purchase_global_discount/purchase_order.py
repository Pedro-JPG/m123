from openerp.osv import fields, osv
from openerp import api
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(osv.Model):
    _inherit = 'purchase.order'



    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        line_obj = self.pool['purchase.order.line']
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax_basica': 0.0,
                'amount_tax_minima': 0.0,
                'amount_total': 0.0,
                'amount_discount':0.0,
                'amount_untaxed_without_discounts':0.0,
            }
            val = val1 = val3= amount_tax_basica=amount_tax_minima=0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                line_price = line_obj._calc_line_base_price(cr, uid, line,
                                                            context=context)
                line_qty = line_obj._calc_line_quantity(cr, uid, line,
                                                        context=context)
                val3 += (line.orig_price_unit * line_qty)  * float(line.discount)/100

                for c in self.pool['account.tax'].compute_all(
                        cr, uid, line.taxes_id, line_price, line_qty,
                        line.product_id, order.partner_id)['taxes']:
                    tax_id = self.pool['account.tax'].browse(cr,uid,line.taxes_id[0].id)

                    if tax_id.name == 'IVA Compras (22%)':
                        amount_tax_basica+=c.get('amount', 0.0)
                    if tax_id.name == 'IVA Compras (10%)':
                        amount_tax_minima+=c.get('amount', 0.0)

            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_tax_basica'] = cur_obj.round(cr, uid, cur, amount_tax_basica)
            res[order.id]['amount_tax_minima'] = cur_obj.round(cr, uid, cur, amount_tax_minima)
            res[order.id]['amount_discount'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['amount_untaxed_without_discounts'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_discount']
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax_basica']+ res[order.id]['amount_tax_minima']
        return res


    @api.multi
    @api.onchange('order_line')
    def compute_total(self):
        res = {}
        cur_obj = self.pool.get('res.currency')
        line_obj = self.pool['purchase.order.line']
        for order in self:
            val = val1 = val3 = amount_tax_basica = amount_tax_minima = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                line_price = line_obj._calc_line_base_price(self._cr, self._uid, line)
                line_qty = line_obj._calc_line_quantity(self._cr, self._uid, line)
                val3 += (line.orig_price_unit * line_qty) * float(line.discount) / 100

                for c in self.pool['account.tax'].compute_all(
                        self._cr, self._uid, line.taxes_id, line_price, line_qty,
                        line.product_id, order.partner_id)['taxes']:
                    tax_id = self.pool['account.tax'].browse(self._cr, self._uid, line.taxes_id[0].id)

                    if tax_id.name == 'IVA Compras (22%)':
                        amount_tax_basica += c.get('amount', 0.0)
                    if tax_id.name == 'IVA Compras (10%)':
                        amount_tax_minima += c.get('amount', 0.0)

            self.amount_untaxed=val1
            self.amount_tax_basica = amount_tax_basica
            self.amount_tax_minima = amount_tax_minima
            self.amount_discount=val3
            self.amount_untaxed_without_discounts= val1 + val3
            self.amount_total = val1 + amount_tax_basica +amount_tax_minima
        return res

    @api.multi
    def button_dummy(self):
        self.compute_total()
        return True

    _columns = {


        'amount_discount': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Descuentos',
                                           multi='sums', store=True, help="The total discount."),

        'amount_untaxed_without_discounts': fields.function(_amount_all, digits_compute=dp.get_precision('Account'),
                                          string='Subtotal',
                                          multi='sums', store=True, help="The amount without tax.",
                                          track_visibility='always'),
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'),
                                          string='Untaxed Amount',
                                          multi='sums', store=True, help="The amount without tax.", track_visibility='always'),
        'amount_tax_basica': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='IVA Tasa Basica',
                                      multi='sums', store=True, help="The tax amount."),
        'amount_tax_minima': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='IVA Tasa Minima',
                                             multi='sums', store=True, help="The tax amount."),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
                                        multi='sums', store=True, help="The total amount."),
    }

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        porcentaje = total=total_descuentos= 0

        for line in order.order_line:
            porcentaje= float(line.discount)

        if porcentaje > 0:

            porcentaje= porcentaje * (-1)
            total_descuentos = order.amount_discount * (-1)


        invoice_vals = super(PurchaseOrder, self)._prepare_invoice(cr, uid, order, lines, context=context)
        invoice_vals.update({
            # 'discount_type': order.discount_type,
            'desc_view1': porcentaje,
            'desc_view1_amount': total_descuentos,
            'amount_tax_basica': order.amount_tax_basica,
            'amount_tax_minima': order.amount_tax_minima,
            # 'amount_discount': total_descuentos

        })
        return invoice_vals


    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        """Collects require data from purchase order line that is used to create invoice line
        for that purchase order line
        :param account_id: Expense account of the product of PO line if any.
        :param browse_record order_line: Purchase order line browse record
        :return: Value for fields of invoice lines.
        :rtype: dict
        """
        _logger.info('pecio sin descuento %s', order_line.orig_price_unit)
        _logger.info('descuento linea %s', order_line.discount)

        return {
            'name': order_line.name,
            'account_id': account_id,
            'price_unit': order_line.orig_price_unit or 0.0,
            'quantity': order_line.product_qty,
            'product_id': order_line.product_id.id or False,
            'uos_id': order_line.product_uom.id or False,
            'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
            'account_analytic_id': order_line.account_analytic_id.id or False,
            'purchase_line_id': order_line.id,
            #'discount': order_line.discount,
        }






