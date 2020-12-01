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
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'amount_discount': 0.0,
                'amount_tax_basica': 0.0,
                'amount_tax_minima': 0.0,
                'amount_untaxed_without_discounts': 0.0
            }
            total_descuento= descuento_linea= amount_tax_basica = amount_tax_minima= subtotal_con_descuentos=0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                descuento_linea=0

                line_price = line_obj._calc_line_base_price(cr, uid, line,
                                                            context=context)
                line_qty = line_obj._calc_line_quantity(cr, uid, line,
                                                        context=context)
                descuento_linea = (line_price *line_qty) * line.discount / 100

                total_descuento+=(line_price *line_qty) * line.discount / 100

                subtotal_con_descuentos += line.price_subtotal

                line_price = line_price - descuento_linea


                #se calcula los impuestos sobre el importe menos el descuento
                for c in self.pool['account.tax'].compute_all(
                        cr, uid, line.taxes_id, line_price, line_qty,
                        line.product_id, order.partner_id)['taxes']:
                    tax_id = self.pool['account.tax'].browse(cr,uid,line.taxes_id[0].id)

                    if tax_id.name == u'IVA Compras (10%)':
                        amount_tax_minima += c.get('amount', 0.0)
                    if tax_id.name == u'IVA Compras (22%)':
                        amount_tax_basica += c.get('amount', 0.0)

            res[order.id]['amount_discount']=cur_obj.round(cr, uid, cur, total_descuento)
            res[order.id]['amount_untaxed_without_discounts']=cur_obj.round(cr, uid, cur, subtotal_con_descuentos - total_descuento)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, subtotal_con_descuentos)
            res[order.id]['amount_tax_basica']=cur_obj.round(cr, uid, cur, amount_tax_basica)
            res[order.id]['amount_tax_minima']=cur_obj.round(cr, uid, cur, amount_tax_minima)
            res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, amount_tax_basica) + cur_obj.round(cr, uid, cur, amount_tax_minima)
            res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res


    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.purchase_order_id.id] = True
        return result.keys()

    _columns = {
        'discount_type': fields.selection([
            ('percent', 'Porcentaje'),
            ('amount', 'Monto')], 'Tipo de descuento'),
        'discount_rate': fields.float('Tasa de descuento', digits_compute=dp.get_precision('Account'),
                                      readonly=True,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, ),
        'amount_discount': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Descuento',
                                           multi='sums', store=True, help="The total discount."),

        'amount_untaxed_without_discounts': fields.function(_amount_all, digits_compute=dp.get_precision('Account'),string='Subtotal',
            multi='sums', store=True, help="Subtotal"),


        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'),
                                          string='Subtotal con descuentos',
                                          multi='sums', store=True, help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
                                      multi='sums', store=True, help="The tax amount."),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
                                        multi='sums', store=True, help="The total amount."),
        'partner_ref':fields.char('Nro Carpeta'),

        'amount_tax_basica': fields.function(_amount_all, digits_compute=dp.get_precision('Account'),
                                          string='IVA Tasa Basica',
                                          multi='sums', store=True, help="IVA Tasa Basica", track_visibility='always'),


        'amount_tax_minima':  fields.function(_amount_all, digits_compute=dp.get_precision('Account'),
                                          string='IVA Tasa Minima',
                                          multi='sums', store=True, help="IVA Tasa Minima", track_visibility='always'),

    }

    _defaults = {
        'discount_type': 'percent',
    }


    @api.multi
    def compute_discount(self, discount):
        line_obj = self.pool['purchase.order.line']
        for purchase in self:
            total_impuestos=total_descuentos = descuento_linea = amount_tax_basica= amount_tax_minima= subtotal_con_descuentos = 0.0
            disc_amnt = 0.0
            for line in purchase.order_line:

                line.discount = discount
                line_price = line_obj._calc_line_base_price(self._cr, self._uid, line)
                line_qty = line_obj._calc_line_quantity(self._cr, self._uid, line)

                subtotal_con_descuentos += line.price_subtotal

                total_descuentos += (line_qty * line_price) * line.discount / 100

                descuento_linea =  (line_qty * line_price) * line.discount / 100

                line_price = line_price - descuento_linea

                for c in self.pool['account.tax'].compute_all(
                        self._cr, self._uid, line.taxes_id, line_price, line_qty,
                        line.product_id, purchase.partner_id)['taxes']:

                    tax_id = self.pool['account.tax'].browse(self._cr, self._uid,line.taxes_id[0].id)
                    if tax_id.name == u'IVA Compras (10%)':
                        amount_tax_minima += c.get('amount', 0.0)
                    if tax_id.name == u'IVA Compras (22%)':
                        amount_tax_basica += c.get('amount', 0.0)

                #disc_amnt += (line.product_qty * line.price_unit * line.discount)/100

            total_impuestos = amount_tax_minima + amount_tax_basica
            total = total_impuestos + subtotal_con_descuentos
            self.currency_id = purchase.pricelist_id.currency_id
            self.amount_discount = total_descuentos
            self.amount_untaxed_without_discounts = subtotal_con_descuentos - total_descuentos
            self.amount_tax = total_impuestos
            self.amount_tax_minima = amount_tax_minima
            self.amount_tax_basica = amount_tax_basica
            self.amount_untaxed = subtotal_con_descuentos
            self.amount_total = total

    @api.onchange('discount_type', 'discount_rate')
    def supply_rate(self):
        for order in self:
            if order.discount_rate >= 0:
                if order.discount_type == 'percent':
                    self.compute_discount(order.discount_rate)
                else:
                    total = 0.0
                    for line in order.order_line:
                        total += (line.product_qty * line.price_unit)
                    if total > 0:
                        discount = (order.discount_rate / total) * 100
                    else:
                        discount=0
                    self.compute_discount(discount)


    @api.multi
    def button_dummy(self):
        self.supply_rate()
        return True

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        """Collects require data from purchase order line that is used to create invoice line
        for that purchase order line
        :param account_id: Expense account of the product of PO line if any.
        :param browse_record order_line: Purchase order line browse record
        :return: Value for fields of invoice lines.
        :rtype: dict
        """
        discount=0
        order = self.pool.get('purchase.order').browse(cr,uid,order_line.order_id.id)
        if order.discount_rate == 0:
            discount = order_line.discount

        return {
            'name': order_line.name,
            'account_id': account_id,
            'price_unit': order_line.price_unit or 0.0,
            'quantity': order_line.product_qty,
            'product_id': order_line.product_id.id or False,
            'uos_id': order_line.product_uom.id or False,
            'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
            'account_analytic_id': order_line.account_analytic_id.id or False,
            'purchase_line_id': order_line.id,
            'discount': discount,
        }
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        porcentaje = total=total_descuentos= 0
        if order.discount_type == 'percent':
            porcentaje = order.discount_rate * (-1)
            total_descuentos = order.amount_discount * (-1)
        else:
            for line in order.order_line:
                total += (line.product_qty * line.price_unit)
            if total > 0:
                porcentaje= (order.discount_rate / total) * 100
                porcentaje = porcentaje * (-1)
                total_descuentos = order.amount_discount * (-1)
        if order.discount_rate == 0:
            porcentaje= 0
            total_descuentos= order.amount_discount * (-1)


        invoice_vals = super(PurchaseOrder, self)._prepare_invoice(cr, uid, order, lines, context=context)
        invoice_vals.update({
            # 'discount_type': order.discount_type,
            'desc_view1': porcentaje,
            'desc_view1_amount': total_descuentos,
            'amount_tax_basica': order.amount_tax_basica,
            'amount_tax_minima': order.amount_tax_minima,
            'amount_discount': total_descuentos

        })
        return invoice_vals

class PurchaseOrderLine(osv.Model):
    _inherit = "purchase.order.line"

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        descuento=0
        for line in self.browse(cr, uid, ids, context=context):
            line_price = self._calc_line_base_price(cr, uid, line,
                                                    context=context)
            line_qty = self._calc_line_quantity(cr, uid, line,
                                                context=context)
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line_price,
                                        line_qty, line.product_id,
                                        line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            descuento= (line_qty * line_price) * line.discount / 100
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total']) - descuento
        return res

    _columns = {
    'discount': fields.float(string='Descuento (%)',
                            digits=(16, 10),
                            # digits= dp.get_precision('Discount'),
                            default=0.0),
    'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute=dp.get_precision('Account')),

    }