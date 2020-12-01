# -*- coding: utf_8 -*-
from openerp import models, fields, api
from openerp.addons.web.controllers.main import serialize_exception,content_disposition

class cliente_form_herencia(models.Model):
    _inherit = 'res.partner'
    grupo = fields.Many2one(comodel_name='dtm.grupo.subgrupo',string='Rubro')
    subgrupo = fields.Many2one(comodel_name='subgrupos.laborales',string='Subrubro')
    forma_pago = fields.Selection([('oca','OCA'),('visa','VISA'),('mastercard','MasterCard'),('abitab','ABITAB'),('redpagos','Red Pagos'),('sede','SEDE'),('cabal','Cabal'),('coor_jubilados','Coor jubilados')])
    nro_cliente = fields.Char(string='Nro Cliente')
    convenio = fields.Char(string='Convenio')
    
    fecha_creacion = fields.Date(string='Fecha Creación')
    fecha_nacimiento = fields.Date(string='Fecha Nacimiento')
    genero = fields.Selection([('masculino','Masculino'),('femenino','Femenino'),('otros','Otros')])
    cantidad_socios = fields.Char(string='Cantidad socios')


    @api.onchange("grupo")
    def filtro_subcategoria(self):
        self.ensure_one()
        lista=[i.id for i in self.grupo]
                               
        return {
            "domain": {
                "subgrupo": [("grupo", "in", lista)],
                }
        } 


