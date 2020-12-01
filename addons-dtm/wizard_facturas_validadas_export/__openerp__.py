# -*- coding: utf-8 -*-
{
    'name': 'Facturas validadas y Facturas Pagas',
    'version': '1.0',
    'author': 'Datamatic',
    'website': 'http://www.datamatic.com.uy',
    'description': """
Facturas validadas y Facturas Pagas.
En contabilidad / Proveedores se crean dos nuevos menus: Facturas validadas y Facturas Pagas. 
    
    """,        
    "depends": ['base', 'account'],
    'data': [
        'wizard_facturas_validadas_export_view.xml',
    ],
    'demo_xml': [],
    'active': False,
    'installable': True,
    'application': True,
}
