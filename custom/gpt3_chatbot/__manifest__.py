# -*- coding: utf-8 -*-
{
    'name': "GPT-3 Chatbot",

    'summary': """
        Integrate GPT-3 Chatbot with Odoo""",

    'description': """
        Long description of module's purpose
    """,

    'license': 'AGPL-3',

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'portal', 'helpdesk'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/assets.xml',
        # 'views/chatbot_template.xml',
        # 'views/menu.xml',
        'views/token_info.xml',
        'views/res_users_form_inherited.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
