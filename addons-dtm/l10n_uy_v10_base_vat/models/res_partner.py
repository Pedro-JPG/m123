# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
import requests





class ResPartner(models.Model):
    _inherit = 'res.partner'


    vat_type = fields.Selection([('2', 'RUT'),
                                 ('3', 'Cédula de identidad'),
                                 ('4', 'Otros'),
                                 ('5', 'Pasaporte'),
                                 ('6', 'DNI'),
                                 ('7', 'NIFE')],
                                string='Tipo de documento',
                                default='2')



    """
    Hacemos obligatorios los campos requeridos para la facturacion electronica

    """

    country_id = fields.Many2one(comodel_name='res.country', required=True)
    street = fields.Char(required=True)
    city = fields.Char(required=True)
    state_id = fields.Many2one(comodel_name='res.country.state', required=True)




    def check_vat_uy(self, vat):
        '''
        Check Uruguayan VAT number (RUT).
        '''
        # One or another ...
        return self.valid_vat_uy(vat) or self.valid_ci_uy(vat)

    def valid_ci_uy(self, ci):
        '''
        Valid Uruguayan CI number.
        '''
        # Only digits
        try:
            int(ci)
        except:
            return False

        ci = str(ci)
        ci = ci.rjust(8, "0")

        if (len(ci) > 8):
            return False

        check_digit = 0
        base = "2987634"
        for i in range(0, 7):
            check_digit += int(ci[i]) * int(base[i])

        check_digit %= 10
        check_digit = 10 - check_digit
        if (check_digit == 10):
            check_digit = 0

        if (check_digit == int(ci[7])):
            return True
        else:
            return False

    def valid_vat_uy(self, vat):
        '''
        Valid Uruguayan VAT number (RUT).
        '''
        # Only digits
        try:
            int(vat)
        except:
            return False

        # Long enough
        if (len(vat) != 12):
            return False

        # VAT[] * Base[]
        check_digit = 0
        base = "43298765432"
        for i in range(0, 11):
            check_digit += int(vat[i]) * int(base[i])

        # Module 11
        check_digit %= 11
        check_digit = 11 - check_digit

        # Mistakes ?
        if (check_digit == 10):
            return False
        else:
            if (check_digit == 11): check_digit = 0
            if (check_digit != int(vat[11])):
                return False

        # We are here, so ...
        return True


