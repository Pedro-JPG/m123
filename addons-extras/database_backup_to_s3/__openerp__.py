# -*- coding: utf-8 -*-
{
    'name': "Auto Database Backup To Amazon S3",

    'summary': """
        Backup database zip or dump files to Amazon S3 Bucket by one click. """,

    'description': """
        With This Module You Can Backup Your Database To Amazon S3 Bucket Directly using The Zip Or Dump Format.
    """,

    'author': "Techspawn Solutions",
    'website': "https://techspawn.com",
    'category': 'Backup',
    'version': '2.0',
    'price': 20.00,
    'currency': 'EUR',
    'external_dependencies': {'python': ['boto']},

    'depends': ['base'],

    'data': [
        'views/s3_backup.xml',
        'views/backup_scheduler.xml',
    ],

    'auto_install': False,
    'installable': True,
    "images": ['static/description/Background.jpg'],
}
