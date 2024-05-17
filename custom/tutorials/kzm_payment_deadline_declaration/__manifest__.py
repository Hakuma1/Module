# -*- coding: utf-8 -*-
{
    'name': "kzm_payment_deadline_declaration",

    'summary': """ kzm_payment_deadline_declaration """,

    'author': "Karizma-conseil",
    'website': "http://www.karizma-conseil.com",
    "license": "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['contacts', 'account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'data/data_sequence.xml',
        'views/res_partner.xml',
        'views/deadline_declaration.xml',
        'views/deadline_declaration_line.xml',
        'views/res_company.xml',
        'views/res_config_settings.xml',
        'wizard/add_invoices_wizard.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
