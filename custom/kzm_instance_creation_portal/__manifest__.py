# -*- coding: utf-8 -*-
{
    'name': "kzm_instance_creation_portal",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mamady Camara",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'kzm_instance_request', 'website', 'portal', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/calendar_portal_view.xml',
        'templates/calendar_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'web.assets_frontend': [
            '/kzm_instance_creation_portal/static/src/js/fullcalendar_integration.js',
            '/kzm_instance_creation_portal/static/src/css/fullcalendar_integration.css',
        ],
    },
}
