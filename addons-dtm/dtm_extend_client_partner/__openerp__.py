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
    'name': 'Extiende Clientes y Proveedores',
    'version': '1.0',
    'website' : 'www.datamatic.com.uy',
    'category': 'Customización',
    'summary': 'Extiende Clientes y Proveedores',
    'description': """
Extiende Clientes y Proveedores
===============================

Este módulo extiende las vistas tree de Clientes y Proveedores


Agrega las siguientes columnas
------------------------------
* Nombre Fantasía
* RUT
* Dirección
""",
    'author': 'Felipe Ferreira',
    'depends': ['dtm_nombre_fantasia'],
    'data': [
        'views/dtm_client_partner_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}