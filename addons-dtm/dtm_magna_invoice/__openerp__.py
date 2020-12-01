# -*- encoding: utf-8 -*-
##########################################################################
#    Copyright (C) OpenERP Uruguay (<http://openerp.com.uy>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Juan Hernandez
#    Planified by: Carlos Lamas
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
    'name': 'Impresion Recibos',
    'version': '1.0',
    'depends': ['base','account','dtm_einvoice_sale'],
    'author': 'Juan Hernandez',
    'website': 'http://www.datamatic.com.uy',
    'category': 'Datamatic',
    'summary': '',
    'description': """
    """,
    'data': [
        'report/report_import.xml',
    ],
    'demo': [
    ],
    'css':[],
    'auto_install': False,
    'installable': True,
    'application': True
}
