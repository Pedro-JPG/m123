# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

import xlwt
from xlsxwriter.workbook import Workbook
from cStringIO import StringIO
import base64
import re,sys
from io import BytesIO
from openerp import api, fields, models
from xlwt import easyxf
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

class debtors_creditor_wizard(models.TransientModel):

    _name ='debtors.creditor.wizard'
    
    company_id =  fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=1)
    debtor_creditor = fields.Selection([('debtor','Deudores / Clientes'),
                                              ('creditor','Acreedores / Proveedores')
                                             ], 'Reporte', default = 'debtor', required=1)
    date_from = fields.Date('From', default = datetime.today().replace(day=1), required=1)
    date_to = fields.Date('To', default = datetime.today(), required=1)
        
    @api.multi
    def get_line_data(self):
        result_acc = []
        temp_lst = {}
        partners = self.env['res.partner'].search([])
        
        for partner in partners: 
            if self.debtor_creditor == 'debtor':
                property = partner.property_account_receivable.id
            else:
                property = partner.property_account_payable.id
                
            movelines = self.env['account.move.line'].search([('partner_id','=',partner.id),('account_id','=',property),('move_id.date','>=',self.date_from),('move_id.date','<=',self.date_to)], order='date')
            
            if movelines:
                for line in movelines:
                    if not temp_lst.has_key(partner.id):
                            tmp = {
                                'code' : partner.ref,
                                'name' : partner.name,
                                'debit' : 0.0,
                                'credit' : 0.0,
                                'balance' : line.debit - abs(line.credit),
                            }
                            temp_lst[partner.id] = [tmp]
                    else:
                        for k,v in temp_lst.iteritems():
                            if k == line.partner_id.id:
                                i = len(v) - 1
                                temp_lst[partner.id][0]['balance'] = v[i]['balance'] + line.debit - abs(line.credit) 
            
        for v in temp_lst.values():
            if not v[0]['balance'] == 0.00:
                v[0]['debit'] = v[0]['balance'] >= 0 and v[0]['balance'] or 0.0
                v[0]['credit'] = v[0]['balance'] < 0 and abs(v[0]['balance']) or 0.0
                result_acc.append(v[0])
        return result_acc
    
    @api.multi
    def print_pdf(self):
        return self.env['report'].get_action(self,'dev_debtors_creditors_listing.debtors_creditord_report')

    @api.multi
    def print_excel(self):
        listing_data = self.get_line_data()
        
        if self.debtor_creditor == 'debtor':
            filename='Debtors/Customers Listing.xls'
        else:
            filename='Creditors/Suppliers.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Listing')
        
        # defining various font styles
        style1= easyxf('font:height 200;align: horiz center;font:bold True;')
        text_center = easyxf('align: horiz center;')
        text_right = easyxf('font:height 200;align: horiz right;font:bold True;')
        
        # setting with of the column
        worksheet.col(4).width = 60 * 60
        worksheet.col(1).width = 120 * 120
        worksheet.col(2).width = 70 * 70
        worksheet.col(3).width = 70 * 70
        
        
        # in merge 1,2 is height[index of cell] ans 1,5 is width[index if cell] 
        if self.debtor_creditor == 'debtor':
            worksheet.write_merge(1, 2, 1, 2, u'Composición Saldo Deudores',easyxf('font:height 380;align: horiz center;font: color blue; font:bold True;'))
        else:
            worksheet.write_merge(1, 2, 1, 2, u'Composición Saldo Acreedores',easyxf('font:height 380;align: horiz center;font: color blue; font:bold True;'))
        
#         writting into the sheet (Labels)
        s_date = datetime.strptime(self.date_from, "%Y-%m-%d").strftime('%d-%m-%Y')
        e_date = datetime.strptime(self.date_to, "%Y-%m-%d").strftime('%d-%m-%Y')
        worksheet.write(1, 3, "Desde",text_right)
        worksheet.write(2, 3, "Hasta",text_right)
        worksheet.write(1, 4, str(s_date))
        worksheet.write(2, 4, str(e_date))
        worksheet.write(5,0, u'Código',style1)
        worksheet.write(5,1, 'Nombre',style1)
        worksheet.write(5,2, 'Debe',style1)
        worksheet.write(5,3, 'Haber',style1)

        seq = 6
        debit_total = []
        credit_total = []
        for counter in range(len(listing_data)):
            if listing_data[counter]['code'] == False:
                listing_data[counter]['code'] = ''
            worksheet.write(seq,0,listing_data[counter]['code'])
            worksheet.write(seq,1, listing_data[counter]['name'])
            if 'debit' in listing_data[counter]:
                worksheet.write(seq,2, listing_data[counter]['debit'])
                debit_total.append(listing_data[counter]['debit'])
            else:
                worksheet.write(seq,2, '0.0',text_center)
            if 'credit' in listing_data[counter]:
                worksheet.write(seq,3, listing_data[counter]['credit'])
                credit_total.append(listing_data[counter]['credit'])
            else:
                worksheet.write(seq,3,'0.0',text_center)
            seq += 1
        z = seq + 1
        dt = sum(debit_total)
        ct = sum(credit_total)
        worksheet.write(z,1,"Total",text_right)
        worksheet.write(z,2,dt)
        worksheet.write(z,3,ct)
        
        
        # exporting excel process
        fp = StringIO()
        workbook.save(fp)
        export_id = self.env['debtors.creditor.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()
        
        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'debtors.creditor.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
            
        }

class debtors_creditor_excel(models.TransientModel):
    _name= "debtors.creditor.excel"
    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
