{
    'name': 'Descuento global en las compras',
    'version': '1.0',
    'category': 'Purchase Management',
    'sequence': 6,
    'summary': "Discount on total in Sale and invoice with Discount limit and approval",
    'author': 'Datamatic',
    'company': 'Datamatic',
    'website': 'http://www.datamatic.com.uy',

    'description': """

Descuento global en las compra
=======================
""",
    'depends': ['sale', 'base', 'stock'],
    'data': [
        'views/purchase_view.xml',
    ],
    'demo': [
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}
