# -*- coding: utf-8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import locale
import time
import logging
import ipdb as pdb
from openerp.exceptions import Warning

class product_product(models.Model):
    _inherit='product.product'

    qty_minimum = fields.Float('Cantidad minima de stock',default=10)
    qty_minimum_hidden = fields.Boolean('mod oculto',store=True,default=True)

    @api.multi
    @api.onchange('virtual_available')
    def get_minimum_hidden(self):
        # pdb.set_trace()
        self.virtual_available_copy = self.virtual_available
        if self.virtual_available_copy > self.qty_minimum:
            self.qty_minimum_hidden = False
        else :
            self.qty_minimum_hidden = True



class listado_stock(models.TransientModel):
    _name = 'listado.stock.minimo'

    listado = fields.Html('testing')
    marca = fields.Many2one('product.brand',string='Marca del producto')
    categ_id = fields.Many2one('product.category',string='Categoria del producto')

    @api.multi
    def generar_planilla(self):
        # pdb.set_trace()
        # Cual informe imprimir
        reporte = self.planilla_resumida()

        # De no haber nada
        if not reporte:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Notificación',
                'params': {
                    'title': 'Reporte',
                    'text': 'Este informe se encuentra en desarrollo.',
                    'sticky': False
                }
            }

        # Mostrar el reporte en pantalla
        self.listado = reporte
        return


    @api.multi
    def planilla_resumida(self):
        # Iniciamos el reporte
        reporte  = ''
        reporte += '<table style="width:100%;">'

        reporte += '   <thead style="border: thin solid gray;">'
        reporte += '        <tr style="border: thin solid gray;">'
        # reporte += '            <th style="border: thin solid gray; text-align: center; width: 10em">        </th>'
        reporte += '            <th style="border: thin solid gray; text-align: center" colspan="7">Planilla de stock minimo</th>'
        # reporte += '            <th style="border: thin solid gray; text-align: center">        </th>'
        # reporte += '            <th style="border: thin solid gray; text-align: center">        </th>'
        # reporte += '            <th style="border: thin solid gray; text-align: center">        </th>'
        # reporte += '            <th style="border: thin solid gray; text-align: center">        </th>'
        reporte += '        </tr style="border: thin solid gray;">'
        reporte += '        <tr>'
        reporte += '            <th style="border: thin solid gray; text-align: center">Nro. Referencia</th>'
        reporte += '            <th style="border: thin solid gray; text-align: center">Nombre</th>'
        reporte += '            <th style="border: thin solid gray; text-align: center; width: 10em">Marca</th>'
        reporte += '            <th style="border: thin solid gray; text-align: center; width: 15em">Categoria</th>'
        reporte += '            <th style="border: thin solid gray; text-align: center; width: 6em">Cantidad disponible</th>'
        reporte += '            <th style="border: thin solid gray; text-align: center; width: 6em">Cantidad Minima</th>'
        reporte += '            <th style="border: thin solid gray; text-align: center; width: 6em">Cantidad Faltante</th>'
        reporte += '        </tr>'
        reporte += '    </thead>'
        reporte += '    <tbody>'

        lista_stock = self.env['product.product'].search([])
       # Para cada producto
        for prod in lista_stock:
            if (not self.categ_id) and (not self.marca):
                if prod.virtual_available <= prod.qty_minimum:
                    reporte += '        <tr style="border-bottom: thin solid gray;">'
                    if prod.default_code:
                        reporte += '            <td>%s</td>' % (prod.default_code)
                    else:
                        reporte += '            <td>  </td>'
                    reporte += '            <td>%s</td>' % (prod.name_template)
                    if prod.product_brand_id.name:
                        reporte += '            <td>%s</td>' % (prod.product_brand_id.name)
                    else:
                        reporte += '            <td>  </td>'
                    if prod.categ_id.name:
                        reporte += '            <td>%s</td>' % (prod.categ_id.name)
                    else:
                        reporte += '            <td>  </td>'
                    reporte += '            <td style="text-align: right">%s</td>' % (prod.virtual_available)
                    reporte += '            <td style="text-align: right">%s</td>' % (prod.qty_minimum)
                    reporte += '            <td style="text-align: right">%s</td>' % ( -(prod.virtual_available - prod.qty_minimum) )
                    reporte += '        </tr>'
            else:
                if (self.categ_id == prod.categ_id) or (self.marca == prod.product_brand_id):
                    if prod.virtual_available <= prod.qty_minimum:
                        # pdb.set_trace()
                        reporte += '        <tr style="border-bottom: thin solid gray;">'
                        if prod.default_code:
                            reporte += '            <td>%s</td>' % (prod.default_code)
                        else:
                            reporte += '            <td>  </td>'
                        reporte += '            <td>%s</td>' % (prod.name_template)
                        if prod.product_brand_id.name:
                            reporte += '            <td>%s</td>' % (prod.product_brand_id.name)
                        else:
                            reporte += '            <td>  </td>'
                        if prod.categ_id.name:
                            reporte += '            <td>%s</td>' % (prod.categ_id.name)
                        else:
                            reporte += '            <td>  </td>'
                        reporte += '            <td style="text-align: right">%s</td>' % (prod.virtual_available)
                        reporte += '            <td style="text-align: right">%s</td>' % (prod.qty_minimum)
                        reporte += '            <td style="text-align: right">%s</td>' % ( -(prod.virtual_available - prod.qty_minimum) )
                        reporte += '        </tr>'




        reporte += '    </tbody>'
        reporte += '</table>'

        return reporte
