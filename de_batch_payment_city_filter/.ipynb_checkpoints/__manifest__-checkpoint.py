# -*- coding: utf-8 -*-
{
    'name': "Batch Payment Filter (city)",

    'summary': """
        Filter city wise partner in batch payment
        """,

    'description': """
        Batch Payment City Filter
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_batch_payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_batch_payment_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
