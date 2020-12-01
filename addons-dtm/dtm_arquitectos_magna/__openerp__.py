# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Adaptación Arquitectos MAGNA",
    "version": "8.0.0.0.0",
    "author": "Datamatic",
    "website": "",
    "category": "",
    "license": "",
    "external_dependencies": {
        'python': [
            'requests',
        ],
    },
    "depends": [
        "base","sale"
    ],
    "data": [
        'views/partner_view.xml',
        'views/sale_order_view.xml',
    ],
    "installable": True,
}
