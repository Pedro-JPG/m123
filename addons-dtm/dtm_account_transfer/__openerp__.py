# -*- coding: utf-8 -*-
{
    'name': 'Dtm - Account Transfer',
    'version': '1.0',
    'author': 'Juan Hernandez - Felipe Ferreira',
    'website': 'http://www.datamatic.com.uy',
    'category': 'Datamatic',
    'summary': 'Correccion de definicion action_confirm del modulo account_transfer.',
    'description': """
    Este modulo hereda la calse account_transfer y corrige la erronea creacion de 
    Asientos analiticos.
    """,
    'depends': ['base', 'account_transfer'],
    'data': [
    ],
    'installable': True,
    'auto_install': False,
}
