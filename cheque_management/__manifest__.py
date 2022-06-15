# -*- coding: utf-8 -*-
{
    'name': 'Cheque Management',
    'version': '14.0',
    'author': 'IBS',
    'category': 'Accounting',
    'description': """cheques management in odoo""",
    'website': '',
    'summary': """""",
    'depends': [
        'base',
        'account',
        'account_accountant',
        'hr',
    ],
    "license": "",
    "price": "",
    "currency": "",
    'data': [
        'security/ir.model.access.csv',
        'views/cheque_management.xml',
        'views/res_config.xml',
        'wizard/cheque_date_wizard_view.xml',

    ],
    'installable': True,
    'auto_install': False,
}
