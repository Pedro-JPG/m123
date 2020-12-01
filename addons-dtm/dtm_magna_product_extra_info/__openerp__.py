# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Datamatic (<http://www.datamatic.com.uy>).
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


{
    'name': 'Magna info presupuestos',
    'version': '1.0',
    'category': '',
    'description': """
    """,
    'author': 'Datamatic',
    'maintainer': 'Datamatic',
    'website': 'http://www.datamatic.com.uy',
    'depends': ['base','account_budget','sale','dtm_arquitectos_magna'],
    'data': [
        'views/product_view.xml',
        'views/sale_order_line_view.xml',
        'report/report_presupuesto.xml',
        'views/account_invoice.xml',
    ],
    'installable': True,

}
