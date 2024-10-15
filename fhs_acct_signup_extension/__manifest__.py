#################################################################################
# File Name: __inti__.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    10/14/2024    Add address fields
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
{
  "name"                 :  "Account Sign-Up Extension",
  "summary"              :  """Add a mandatory field for users to input phone number, address, and contractor/fiscal position attachments during sign up.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "FHS - G.S.S.",
  "depends"              :  ['auth_signup'],
  "data"                 :  [
                             'views/fhs_acct_signup_extension.xml',
                             #'views/res_partner_view.xml',  # This file is used to create page 'tabs' with the attachments, not need if not wanted
                            ],
  "images"               :  ['static/description/fhs.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  #"pre_init_hook"        :  "pre_init_check",
}
