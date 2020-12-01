##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    moneda_costo_id = fields.Many2one(
        'res.currency', 'Moneda Costo')

    # price fields
    precio_costo_original = fields.Float(
        'Precio de Costo',
        digits=dp.get_precision('Product Price'))

    tipo_cambio_usado = fields.Float(
        'Tipo de Cambio',
        digits=dp.get_precision('Product Price'))

    @api.one
    @api.depends('precio_costo_original','tipo_cambio_usado')
    def _compute_standard_price(self):

        if self.precio_costo_original and self.tipo_cambio_usado:
            self.standard_price = self.precio_costo_original * self.tipo_cambio_usado
        else:
            self.standard_price = 0
