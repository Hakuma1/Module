# -*- coding: utf-8 -*-
{
    'name': "STAMP DUTIES",

    'summary': """STAMP DUTIES""",

    'author': "Camara Mamady",
    'website': "",
    "license": "AGPL-3",
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/pos_payment_method.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'point_of_sale.assets': [
            'stamp_duties/static/src/xml/PaymentScreenPaymentLines.xml',
            'stamp_duties/static/src/js/*.js',
        ],
    },
}
