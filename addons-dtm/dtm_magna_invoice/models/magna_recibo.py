# -*- coding: utf-8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import locale
import time
import ipdb as pdb
from openerp.exceptions import Warning


class account_voucher(models.Model):
    _inherit='account.voucher'

    @api.multi
    def invoice_print(self):
        return self.env['report'].get_action(self, 'account_vanacity')
        
    fecha_fmt = fields.Char('Fecha formateada para impresion',readonly=True,compute='_date_fmt')

    @api.multi
    def get_fact_actual(self, move_line_id):
        invoice = move_line_id.invoice
        serie = invoice.fe_Serie + " " + str(invoice.fe_DocNro)
        return serie

    @api.one
    def get_moneda_literal(self):
        if self.journal_id.currency:
            return "DOLARES AMERICANOS"
        else:
            return "PESOS URUGUAYOS"

    @api.one
    def _date_fmt(self):
        fecha = time.strptime(self.date,DEFAULT_SERVER_DATE_FORMAT)
        meses = {'01':'Enero',
        '02':'Febrero',
        '03':'Marzo',
        '04':'Abril',
        '05':'Mayo',
        '06':'Junio',
        '07':'Julio',
        '08':'Agosto',
        '09':'Septiembre',
        '10':'Octubre',
        '11':'Noviembre',
        '12':'Diciembre',}
        res = "%02d de %02s de %4d" % (fecha.tm_mday,meses[str(fecha.tm_mon)],fecha.tm_year)
        self.fecha_fmt = res


    def monto_literal(self, numero):
        # Datos auxiliares
        UNIDADES = (
            '',
            'UN ',
            'DOS ',
            'TRES ',
            'CUATRO ',
            'CINCO ',
            'SEIS ',
            'SIETE ',
            'OCHO ',
            'NUEVE ',
            'DIEZ ',
            'ONCE ',
            'DOCE ',
            'TRECE ',
            'CATORCE ',
            'QUINCE ',
            'DIECISEIS ',
            'DIECISIETE ',
            'DIECIOCHO ',
            'DIECINUEVE ',
            'VEINTE '
        )
        DECENAS = (
            'VEINTI',
            'TREINTA ',
            'CUARENTA ',
            'CINCUENTA ',
            'SESENTA ',
            'SETENTA ',
            'OCHENTA ',
            'NOVENTA ',
            'CIEN '
        )
        CENTENAS = (
            'CIENTO ',
            'DOSCIENTOS ',
            'TRESCIENTOS ',
            'CUATROCIENTOS ',
            'QUINIENTOS ',
            'SEISCIENTOS ',
            'SETECIENTOS ',
            'OCHOCIENTOS ',
            'NOVECIENTOS '
        )
        UNITS = (
            ('', ''),
            ('MIL ', 'MIL '),
            ('MILLON ', 'MILLONES '),
            ('MIL MILLONES ', 'MIL MILLONES '),
            ('BILLON ', 'BILLONES '),
            ('MIL BILLONES ', 'MIL BILLONES '),
            ('TRILLON ', 'TRILLONES '),
            ('MIL TRILLONES', 'MIL TRILLONES'),
            ('CUATRILLON', 'CUATRILLONES'),
            ('MIL CUATRILLONES', 'MIL CUATRILLONES'),
            ('QUINTILLON', 'QUINTILLONES'),
            ('MIL QUINTILLONES', 'MIL QUINTILLONES'),
            ('SEXTILLON', 'SEXTILLONES'),
            ('MIL SEXTILLONES', 'MIL SEXTILLONES'),
            ('SEPTILLON', 'SEPTILLONES'),
            ('MIL SEPTILLONES', 'MIL SEPTILLONES'),
            ('OCTILLON', 'OCTILLONES'),
            ('MIL OCTILLONES', 'MIL OCTILLONES'),
            ('NONILLON', 'NONILLONES'),
            ('MIL NONILLONES', 'MIL NONILLONES'),
            ('DECILLON', 'DECILLONES'),
            ('MIL DECILLONES', 'MIL DECILLONES'),
            ('UNDECILLON', 'UNDECILLONES'),
            ('MIL UNDECILLONES', 'MIL UNDECILLONES'),
            ('DUODECILLON', 'DUODECILLONES'),
            ('MIL DUODECILLONES', 'MIL DUODECILLONES'),
        )

        # Funciones auxiliares
        def hundreds_word(number):
            converted = ''
            if not (0 < number < 1000):
                return 'No es posible convertir el numero a letras'

            number_str = str(number).zfill(9)
            cientos = number_str[6:]

            if (cientos):
                if (cientos == '001'):
                    converted += 'UN '
                elif (int(cientos) > 0):
                    converted += '%s ' % __convert_group(cientos)

            return converted.title().strip()

        def __convert_group(n):
            output = ''

            if (n == '100'):
                output = "CIEN "
            elif (n[0] != '0'):
                output = CENTENAS[int(n[0]) - 1]

            k = int(n[1:])
            if (k <= 20):
                output += UNIDADES[k]
            else:
                if ((k > 30) & (n[2] != '0')):
                    output += '%sY %s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
                else:
                    output += '%s%s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])

            return output

        def to_word(number, mi_moneda=None):
            human_readable = []
            num_units = format(number, ',').split(',')
            # print num_units
            for i, n in enumerate(num_units):
                if int(n) != 0:
                    words = hundreds_word(int(n))
                    units = UNITS[len(num_units) - i - 1][0 if int(n) == 1 else 1]
                    human_readable.append([words, units])

            # filtrar MIL MILLONES - MILLONES -> MIL - MILLONES
            for i, item in enumerate(human_readable):
                try:
                    if human_readable[i][1].find(human_readable[i + 1][1]):
                        human_readable[i][1] = human_readable[i][1].replace(human_readable[i + 1][1], '')
                except IndexError:
                    pass
            human_readable = [item for sublist in human_readable for item in sublist]
            return ' '.join(human_readable).replace('  ', ' ').title().strip()

        # Conversión
        locale.setlocale(locale.LC_ALL,'')
        temp1 = locale.format('%10.2f',(numero-int(numero)),grouping=True)[-2:]
        valorentero = int(numero)
        valordecimal = int((numero-int(numero))*100)
        if (valordecimal!=0):
            return to_word(valorentero).upper() + " CON " + temp1 + "/100"
        else:
            return to_word(valorentero).upper()

    @api.one
    def currency_fmt(self,value):
        locale.setlocale(locale.LC_ALL,'')
        return str(locale.format('%10.2f',value,grouping=True))


