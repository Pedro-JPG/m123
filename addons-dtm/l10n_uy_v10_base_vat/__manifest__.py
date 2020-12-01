# -*- coding: utf-8 -*-
{
    'name' : 'Validador RUT/CI Uruguay',
    'version' : '1.0.0',
    'author' : 'Datamatic',
    'category' : 'Generic Modules/Base',
    'summary': 'Valida RUT y CI.',
    'description' : """
Validador RUT y CI
-----------------------

Créditos:
---------
Este módulo esta basado en el módulo de Alex Cuellar en https://github.com/alexcuellar/l10n_pe_doc_validation

    """,
    'website': 'www.datamatic.com.uy',
    'depends' : ['account','base_vat'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'qweb' : [

    ],
    'demo': [
        #'demo/account_demo.xml',
    ],
    'test': [
        #'test/account_test_users.yml',
    ],
    'images': [
       
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "sequence": 1,
}


