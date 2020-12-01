# -*- encoding: utf-8 -*-
##########################################################################
#    Copyright (C) OpenERP Uruguay (<http://openerp.com.uy>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Felipe Ferreira
#    Planified by: Felipe Ferreira
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
    'name': 'Filtro Metodos de Pago',
    'version': '1.0',
    'website' : 'www.datamatic.com.uy',
    'category': 'Personalización',
    'summary': 'Filtro',
    'description': """
Filtro de metodos de pagos de clientes y proveedores

""",
    'author': 'Felipe Ferreira',
    'depends': ['base', 'account','account_check_writing'],
    'data': [
        'views/dtm_filtro_payment_method_view.xml',
        'views/account_voucher_vendor_payment_method_form.xml',
        'views/account_invoice_tree.xml',
        'views/account_invoice_form_ext.xml',
        'views/account_check_writing.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
