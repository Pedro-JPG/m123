# -*- coding: utf_8 -*-
from openerp.osv import fields, osv
import time
import logging
import lxml.etree as et
from suds import WebFault
from suds.client import Client

from openerp import models, api, fields, _
from openerp.exceptions import except_orm
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from qrcode import *
import tempfile
import base64
import ipdb as pdb
from datetime import date, timedelta
from ..library import formatters

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    formatter = formatters.Formatters()

    rut_factura = fields.Char(string = 'rut sin prefijo de pais',compute="get_rut_fact")
    doct_type = fields.Char(string = 'Tipo de documento', compute="get_doc_type")
    tipo_pago = fields.Char(string='Forma de Pago', compute="get_doc_type")
    DgiParam = fields.Char(string=u'Resolución DGI')
    num_orig = fields.Char(string='Doc. Origen', compute='get_num_orig')


    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.sent = True
        return self.env['report'].get_action(self, 'dtm_fe_invoice.fe_invoice_report')

    @api.multi
    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        template = self.env.ref('dtm_fe_invoice.dtm_email_template_edi_invoice', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.one
    def get_num_orig(self):
        if self.type == 'out_refund':
            self.num_orig = self.env['account.invoice'].search([('number','=',self.origin)]).fe_DocNro
        else:
            self.num_orig = self.origin
    @api.one
    def get_rut_fact(self):
        self.rut_factura = self.partner_id.vat[2:]

    @api.multi
    @api.depends('name','doct_type')
    def get_doc_type(self):
        tipos_documento = {
            '2': 'RUT',
            '3': 'Cédula de identidad',
            '4': 'Otros',
            '5': 'Pasaporte',
            '6': 'DNI',
            '7': 'NIFE'
        }
        for recs in self:
            # Facturas de Cliente
            if recs.partner_id:
                if recs.type == 'out_invoice':
                    if recs.partner_id.vat:
                        if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'RUT':
                            recs.doct_type = 'e-Factura'
                        if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'Cédula de identidad':
                            recs.doct_type = 'e-Ticket'
                        if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'Otros' and recs.partner_id.country_id.code != 'UY':
                            recs.doct_type = 'e-Ticket'
                #Notas de Credito
                if recs.type == 'out_refund':
                    if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'RUT':
                        recs.doct_type = 'Nota de Credito de e-Factura'
                    if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'Cédula de identidad':
                        recs.doct_type = 'Nota de Credito de e-Ticket'
                    if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'Otros' and recs.partner_id.country_id.code != 'UY':
                        recs.doct_type = 'Nota de Credito de e-Ticket'

                #Notas de Debito
                if recs.is_debit_note:
                    if recs.type == 'out_invoice' and recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'RUT':
                        recs.doct_type = "Nota de Debito de e-Factura"
                    if recs.partner_id.vat_type in tipos_documento and tipos_documento[recs.partner_id.vat_type] == 'Cédula de identidad':
                        recs.doct_type = "Nota de Debito de e-Ticket"

            sys_cfg = recs.env['ir.config_parameter']
            #Aprovecho para sacar del parametro de sistema el valor de la resolución DGI para cada cliente
            SysParam = self.env['ir.config_parameter']
            if SysParam.get_param('fe_resolucion_DGI'):
                self.DgiParam = SysParam.get_param('fe_resolucion_DGI')

            if recs.payment_term.name == 'Contado':
                recs.tipo_pago = 'Contado'
            else:
                recs.tipo_pago = 'Crédito'

    @api.multi
    def make_csv(self):
        facturas_cliente = self.env['account.invoice'].search([('state', '!=', 'draft'), ('state', '!=', 'cancel'), ('type', '=', 'out_invoice')], order='partner_id')
        notas_credito = self.env['account.invoice'].search([('state', '!=', 'draft'), ('state', '!=', 'cancel'), ('type', '=', 'out_refund')])
        #de la factura necesito quedarme con el impuesto
        #del asiento el impuesto en ambas monedas, generalmente es la segunda linea de asiento
        #datos que van a fuego
        rut = 212227280012
        formulario = '02181'
        anomes = 201701
        iva = 502
        csv = []
        for factura in facturas_cliente:
            if factura.partner_id.vat:
                for fac in factura.invoice_line:
                    if fac.invoice_line_tax_id.id == 1:
                        string = str(factura.number or '') + ';' + str(rut or '') + ';' + str(formulario or '') + ';' + str(anomes or '') + ';' + str(factura.partner_id.vat[2:] or '') + ';' + str(anomes or '') + ';' + str(iva or '') + ';' + str(factura.move_id.line_id[1].credit or '') + ';' + str(factura.amount_tax or '') + ';' + str(factura.currency_id.name or '')
                    csv.append(string)
            #print factura.number

        # for nota in notas_credito:
        #     string = ""
        #     string = str(nota.date_invoice or '') + ';' + str(nota.number or '') + ';' + str(
        #         nota.amount_tax) + ';' + str(
        #         nota.move_id.line_id[1].debit) + ';' + str(nota.amount_untaxed or '')+ ';' + str(nota.currency_id.name or '')
        #     csv.append(string)
        return csv



    @api.multi
    def build_and_save(self):
        data_to_save = ""
        csv = self.make_csv()
        data_to_save += 'FACTURA; RUTINCO; FORUMLARIO; ANIOMES; RUTCLIENTE; ANIOMES; TASA BASICA; IVA FACTURADO PESOS; IVA FACTURADO DOLARES; MONEDA''\n'
        for i in csv:
            data_to_save = data_to_save + i
            data_to_save = data_to_save + '\n'

        # data_to_save=codecs.encode(data_to_save,'latin1')
        data_to_save = base64.encodestring(data_to_save)
        # Nombre para el archivo
        file_name = "datos_datos.csv"

        # Aqui se crea el wizard que contendrá
        # el enlace de descarga.
        wiz_id = self.env['export.to.csv'].create({'name': file_name, 'archive': data_to_save})
        return {
            'name': "Save File",
            'type': 'ir.actions.act_window',
            'res_model': 'export.to.csv',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz_id.id,
            'views': [(False, 'form')],
            'target': 'new',
        }




