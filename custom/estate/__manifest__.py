# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'summary': """
        This module is created for real estate management""",

    'description': """
        This module is created for real estate management
    """,

    'author': "Mamady Camara",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/estate_property_type_data.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/inherited_res_users.xml',
        'views/estate_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'application': True,
    'sequence': -110,
}
