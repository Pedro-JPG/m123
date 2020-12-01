# -*- coding: utf-8 -*-


from openerp import api, fields, models
#import ipdb as pdb

class res_partner(models.Model):
    _inherit = 'res.partner'

    es_arquitecto = fields.Boolean(string='Arquitecto', default=False)

