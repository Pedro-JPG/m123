# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012  Carlos Lamas Bruzzone
#
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
#
##############################################################################

{
    'name': 'Banks of Uruguay',
    'version': '1.0',
    'author': 'Datamatic',
    'category': 'Localisation/Uruguay',
    'website': 'http://www.datamatic.com.uy/',
    'license': 'GPL-3',
    'description': """
Módulo de Localización Uruguaya
Incluye:
 - Entidades Bancarias en Uruguay
 
""",
    'depends': ['base','l10n_uy_states',],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': ['data/res_bank.xml',],
    'active': False,
    'installable': True,
}
