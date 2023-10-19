# -*- coding: utf-8 -*-
{
    'name': "IBS Stock Move Effective Date",
    'summary': """""",
    'description': """Stock Move Effective Date Can Be Filter In Product Moves Report""",
    'author': "Younis Mostafa Khalaf",
    'website': "",
    'category': 'Stock',
    'version': '15.0',
    'sequence': '1',
    'depends': [
        'base',
        'stock',
    ],
    # always loaded
    'data': [
        'views/stock_move.xml',
    ],
}
