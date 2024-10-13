{
    'name': 'Custom Purchase Order Report',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Customizations to Purchase Order Report',
    'depends': ['purchase', 'web'],
    'data': [
        'views/report_purchase_order.xml',
    ],
    'installable': True,
    'application': False,
}
