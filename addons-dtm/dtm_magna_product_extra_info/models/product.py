# -*- coding: utf_8 -*-

import unicodedata
import sys
import csv
import calendar
import time
import subprocess
import os
from os.path import basename,isfile
import string
import random
#import ipdb as pdb
import math
import base64
import datetime
import cPickle as pickle
import locale
import codecs

import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _, http
from openerp.exceptions import Warning, ValidationError
from openerp.modules import get_module_path
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition



class product_template(models.Model):
    _name = "product.template"
    _inherit = "product.template"


    extra_info = fields.Text(string="Descripción para presupuesto")
    mano_obra = fields.Boolean(string=u'Mano de Obra de Instalación')