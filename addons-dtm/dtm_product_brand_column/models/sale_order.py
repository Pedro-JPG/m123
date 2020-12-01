# -*- encoding: utf-8 -*-
##########################################################################
#    Copyright (C) OpenERP Uruguay (<http://openerp.com.uy>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Juan Hernandez
#    Planified by: Juan Hernandez
#    Finance by: Datamatic S.A. - www.datamatic.com.uy
#    Audited by: Carlos Lamas
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

from datetime import timedelta
#from openerp import models, fields, api, exceptions
# import ipdb as pdb
import datetime

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import Warning
from openerp.modules import get_module_path


class sale_order_line(models.Model):
    _inherit="sale.order.line"

    prod_brand_id = fields.Many2one('product.brand',required=True,readonly=True,string='Product Brand',related='product_id.product_tmpl_id.product_brand_id')

class purchase_order_line(models.Model):
    _inherit="purchase.order.line"

    prod_brand_id = fields.Many2one('product.brand',required=True,readonly=True,string='Product Brand',related='product_id.product_tmpl_id.product_brand_id')
