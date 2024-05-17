# -*- coding: utf-8 -*-
{

    'name': "Instance",

    'summary': "Instance management",

    'license': 'LGPL-3',

    'author': "Camara Mamady",
    'website': "https://github.com/MC-Karizma/Test_Module_Odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal', 'contacts', 'sale_management', 'hr', 'sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/create_instance_wizard.xml',
        'data/activity.xml',
        'data/data_sequence.xml',
        'data/kzm_instance_request_mail_template.xml',
        'data/kzm_instance_request_mail_template2.xml',
        'views/kzm_instance_request_views.xml',
        'views/employee.xml',
        'views/res_config_setting.xml',
        'views/devis.xml',
        'views/odoo_version_views.xml',
        'views/perimeter.xml',
        'data/data_odoo_version.xml',
        'data/data_perimeter.xml',
        'report/sale_report_inherit.xml',
        'report/report_instance.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': 'False',
    'sequence': -100,
    "qweb": [

    ],
    "assets": {
        "web.assets_backend": [
            "kzm_instance_request/static/src/js/widget_one.js",
            "kzm_instance_request/static/src/js/widget_two.js",
            "kzm_instance_request/static/src/xml/widget_one_template.xml",
        ],
    },
}
