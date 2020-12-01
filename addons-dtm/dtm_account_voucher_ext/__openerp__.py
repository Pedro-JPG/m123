# -*- encoding: utf-8 -*-
##########################################################################
#    Copyright (C) OpenERP Uruguay (<http://openerp.com.uy>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Felipe Ferreira, Emilio Fernandez
#    Planified by: Felipe Ferreira, Emilio Fernandez
#    Finance by: Datamatic S.A. - www.datamatic.com.uy
#
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
{
    'name' : 'Extensiones de Datamatic al modulo Facturacion en Linea',
    'version': '1.0',
    'website' : 'www.datamatic.com.uy',
    'category': 'Accounting & Finance',
    'summary': 'Extensiones al modulo de facturacion en linea',
    'description': """
Extensiones al modulo de facturacion en linea
=============================================
Cambios en el Modelo
--------------------
* Hace obligatorio el campo Ref de Pago
* Carga de forma automatica el diario segun la cuenta del cliente
""",
    'author': 'Datamatic',
    'depends': ['base','account','account_voucher','dtm_payment_method_filter','account_followup'],
    'data': [
        'views/voucher_payment_receipt_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
