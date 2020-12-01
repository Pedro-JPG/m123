from openerp import models, fields, api
import logging
from datetime import datetime
#from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)
from openerp.exceptions import except_orm, Warning, RedirectWarning

class purchase_global_discount_wizard(models.TransientModel):
    _name = "purchase.order.global_discount.wizard"

    # todo implement fixed amount
    type = fields.Selection([
         ('percentage', 'Porcentaje')
         ],
         'Tipo de descuento',
         required=True,
         default='percentage',
         )
    amount = fields.Float(
        # 'Amount',
        'Tasa de descuento',
        required=True,
        )

    @api.multi
    def confirm(self):
        self.ensure_one()
        order = self.env['purchase.order'].browse(
            self._context.get('active_id', False))

        if self.type == 'percentage':
            if self.amount > 100:
                raise Warning("El porcentaje maximo de descuento es 100%")
            for line in order.order_line:
                line.discount = str(self.amount)
                line.price_unit = line.orig_price_unit * (1 - (self.amount or 0.0) / 100.0)
        else:
            total_amount = order.amount_untaxed
            for line in order.order_line:
                line.discount = ((line.price_subtotal / total_amount) * self.amount) / line.product_qty
                line.price_unit = float(line.orig_price_unit) - float(line.discount)
        return True
