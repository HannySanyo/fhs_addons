#################################################################################
# File Name: __init__.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/08/2024    Add company name and address fields
#                    G. Sanyo    09/29/2024    Creation
#################################################################################

{
    "name": "Account Sign-Up Extended",
    "summary": """Add additional fields during account sign-up, such as phone, address, attachments, etc.""",
    "category": "Website",
    "version": "1.0.0",
    "sequence": 1,
    "author": "FHS - G.S.S.",
    "depends": ['auth_signup'],
    "data": [
        'views/acct_signup_extension_view.xml',
        # 'views/res_partner_view.xml',  # Uncomment if needed
    ],
    "assets": {
        'web.assets_frontend': [
            'static/src/js/dynamic_fields.js',
        ],
    },
    "images": ['static/description/fhs.png'],
    "application": True,
    "installable": True,
    "auto_install": False,
}