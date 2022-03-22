# -*- coding: utf-8 -*-
{
    'name': "Tattoo",
    'summary': "Management of a Tattoo Store",
    'description': "",
    'sequence': 1,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base_setup'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/tattoo_session_views.xml',
        'views/tattoo_appointment_views.xml',
        'views/tattoo_design_views.xml',
        'views/tattoo_menuitem.xml',
        'views/css_loader.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}