# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#     Copyright (C) 2012 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
# import ipdb as pdb

class account_voucher_uy(models.Model):

    _inherit = 'account.voucher'
    _description = 'Accounting Voucher, extension'


    @api.one
    def action_cancel(self):
        voucher_obj = self.env['account.voucher']
        move_obj = self.env['account.move']
        for voucher in self.voucher_ids:
            voucher.unlink()
        if self.adjust_move:
            self.adjust_move.unlink()
        return self.write({'state':'cancel'})

    @api.one
    def proforma_voucher(self):
        if self.writeoff_amount != 0 and self.payment_option != 'with_writeoff':
            raise exceptions.Warning(_('User Error!'),u"no se puede validar un pago con diferencia distinta de cero sin contrapartida. Seleccione la contrapartida o modifique el importe")
        else:
            return super(account_voucher_uy,self).proforma_voucher()


    @api.one
    def button_setear_vacio(self):
        for line in self.line_ids:
            line.reconcile = 0
            line.amount = 0.0

    @api.multi
    def button_get_nro_dgi(self):
        for recs in self.line_ids:
            if bool(recs.move_line_id.invoice.fe_Serie) and recs.move_line_id.invoice.fe_DocNro:
                recs.nro_factura = recs.move_line_id.invoice.fe_Serie + ' ' + str(recs.move_line_id.invoice.fe_DocNro)
        return

    @api.multi
    def button_eleminar_no_conciliado(self):
        for line in self.line_ids:
            if not line.amount:
                self.write({'line_ids': [(3,line.id,_)],})

    # def write ( self, cr, uid, ids, values, context = None ):
    @api.one
    def write ( self, values ):
        if not values.get ( 'vendedor_id' ):
            values.update ({ 'vendedor_id' : self.partner_id.user_id.id })
            values.update ({ 'vendedor_name' : self.partner_id.user_id.name })
        return super (account_voucher_uy, self ).write(values)

    vendedor_id = fields.Integer ( 'Vendor ID' )
    vendedor_name = fields.Char ( 'Vendor name' )

account_voucher_uy()



class account_voucher_line(models.Model):
    _inherit = 'account.voucher.line'
    _description = 'Accounting Voucher, extension'

    @api.multi
    def get_nro_dgi(self):
        for recs in self:
            if bool(recs.move_line_id.invoice.fe_Serie) and recs.move_line_id.invoice.fe_DocNro:
                recs.nro_factura = recs.move_line_id.invoice.fe_Serie + ' ' + str(recs.move_line_id.invoice.fe_DocNro)
        return


    nro_factura = fields.Char(string='Nro DGI', compute='get_nro_dgi', store=True)
