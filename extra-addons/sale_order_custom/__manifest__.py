# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Order Custom',
    'version': '1.0',
    'category': 'Sales/sale_order_custom',
    'sequence': -100,
    'summary': 'custom',
    'description': "custom",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base_setup',
        'sale_management'
    ],
    'data': [
        'views/sale_views.xml',
        'report/sale_report_templates.xml',
    ],
    'demo': [],
    'qweb': [],
    'css': ['static/src/css/custom-css.css'],
    'application': True,
    'installable': True,
    'auto_install': False
}