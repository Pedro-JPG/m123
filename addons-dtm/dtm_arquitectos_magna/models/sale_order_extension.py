# -*- coding: utf-8 -*-


from openerp import api, fields, models
#import ipdb as pdb

class sale_order(models.Model):
    _inherit = 'sale.order'

    arquitecto_id = fields.Many2one('res.partner',string='Arquitecto',domain=[('es_arquitecto','=',True)])

