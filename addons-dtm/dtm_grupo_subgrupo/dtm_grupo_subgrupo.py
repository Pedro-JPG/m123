# -*- coding: utf_8 -*-
from openerp import models, fields, api



class dtm_grupo_subgrupo(models.Model):
    _name = 'dtm.grupo.subgrupo'
    _rec_name = 'grupos'
    grupos = fields.Char(string='Rubros')
    subgrupo = fields.One2many(comodel_name='subgrupos.laborales',inverse_name='grupo',string='Subrubro', readonly=True)



class subgrupos_laborales(models.Model):
    _name = 'subgrupos.laborales'
    _description = 'Subgrupos'
    _rec_name = 'subgrupo'
    grupo = fields.Many2one(comodel_name='dtm.grupo.subgrupo',string='Rubro padre')
    subgrupo = fields.Char(string='Nombre del Subrubro')









    