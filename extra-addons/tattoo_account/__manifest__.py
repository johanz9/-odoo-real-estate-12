# -*- coding: utf-8 -*-
{
    'name': "Tattoo Account",
    'summary': "Tattoo account",
    'description': "",
    'sequence': 2,
    'author': "johanz9",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'tattoo',
        'account'
    ],

    # always loaded
    'data': [

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}