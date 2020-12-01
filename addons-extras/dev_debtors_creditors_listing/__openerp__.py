# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################
{
    'name': 'Debtors/Creditors Listing Report',
    'summary': 'App will Print Debtors/Creditors Listing on specific dates into PDF-Excel format',
    'version': '8.0.1.0',
    'sequence':1,
    'category': 'Account',
    'description': """
                   App will Print Debtors/Creditors Listing on specific dates into pdf-excel format

        Debtors reports, Creditors Report, Debtors listing report, Creditors listing report,Debtors note , Creditors note, 
Debtors invoice, Debtors refunds, Creditors invoice, Creditors refund, Creditors vendor bills, vendor refunds
                    """,
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['sale','account'],
    'data': [
       'wizard/debtors_creditors_wizard.xml',
       'report/deb_cre_report_template.xml',
       'report/deb_cre_report_menu.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':49.0,
    'currency':'EUR',
#    'live_test_url':'https://youtu.be/A5kEBboAh_k',
}


