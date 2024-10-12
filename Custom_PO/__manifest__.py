{
    'name': 'Custom Purchase Order Report',
    'version': '1.0',
    'category': 'Purchase',
    'summary': 'Customizations to the Purchase Order report',
    'description': """
        This module customizes the purchase order report to include custom shipping address information.
    """,
    'author': 'Your Name',
    'depends': ['purchase', 'purchase_stock'], 
    'data': [
        'views/purchase_order_view.xml', 
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
