# -*- coding: utf-8 -*-
import ipdb as pdb
import datetime
from openerp import models, fields, api, _
import logging
import time
import csv
from StringIO import StringIO
import base64
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class carga_oportunidades(models.TransientModel):

    _name = 'carga_oportunidades'
    _description = "Carga de oportunidades"

    archive = fields.Binary(string='Archivo')

    @api.multi
    def ingresa_oportunidades(self):
        """
        row[1] - Fecha
        row[2] - Nombre
        row[3] - Producto
        row[4] - Producto 2
        row[5] - Producto 3
        row[6] - Estado

        """

        entrada = StringIO ()
        base64.decode (StringIO (self.archive), entrada )
        entrada.seek (0)
        spamreader = csv.reader(entrada, delimiter=',', quotechar='"')
        csv_file = []
        user_id = self.env['res.users'].search([('name','=','Bruno Peixoto')])

        # pdb.set_trace ()

        next(spamreader,None)
        for row in spamreader:

            if not row:
                continue

            nombre_producto=False
            nombre_producto_dos=False
            nombre_producto_tres=False
            values={}
            product_id=False
            productos = []
            fecha=False
            if row[1]:
                fecha = row[1]

            # if '' in set (row):
            #     continue
            # apunte = False
            # import sys
            # reload (sys)

            values['fecha_propuesta'] = fecha
            values['name'] = row[2]
            values['user_id']= user_id.id

            if row[3]:
                nombre_producto = row[3]
            if row[4]:
                nombre_producto_dos = row[4]
            if row[5]:
                nombre_producto_tres = row[5]

            values['stage_id']= self.env['crm.case.stage'].search([('name','=',row[6])]).id

            if nombre_producto:
                product_id = self.env['product.product'].search([('name','like',nombre_producto)],limit=1)
                if len(product_id)>0:
                    productos.append((0,0,{
                    'product_id': product_id.id,
                    'price':0.0,
                    # 'crm_lead_id':crm_lead_id,
                    }))

            if nombre_producto_dos:
                product_id = self.env['product.product'].search([('name','like',nombre_producto_dos)],limit=1)
                if len(product_id)>0:
                    productos.append((0,0,{
                    'product_id': product_id.id,
                    'price':0.0,
                    # 'crm_lead_id':crm_lead_id,
                    }))

            if nombre_producto_tres:
                product_id = self.env['product.product'].search([('name','like',nombre_producto_tres)],limit=1)
                if len(product_id)>0:
                    productos.append((0,0,{
                    'product_id': product_id.id,
                    'price':0.0,
                    # 'crm_lead_id':crm_lead_id,
                    }))

            values['product_ids'] = productos
            values['type']='opportunity'
            values['stage_type']='opportunity'
            # Crear la opotunidad con los productos
            crm_lead_id = self.env['crm.lead'].create(values) 



class export_to_csv(models.TransientModel):
    _name = 'export.to.csv'
    _description = 'Wizard to save a file'
    _rec_name = 'name'

    name = fields.Char(string='Name' ,readonly=True)
    archive = fields.Binary(string='Save File',readonly=True)


export_to_csv()
