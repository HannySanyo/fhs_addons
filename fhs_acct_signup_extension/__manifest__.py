#################################################################################
# File Name: __inti__.py
# Revision History:  Engineer    Date          Description
#                    G. Sanyo    09/29/2024    Creation
#################################################################################
{
  "name"                 :  "Account Sign-Up Extended",
  "summary"              :  """Add a mandatory field for users to input their phone number and optional attachments for contractors and those tax exempt during account sign up.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "FHS - G.S.S.",
  "depends"              :  ['auth_signup'],
  "data"                 :  [
                             'views/account_details_template.xml',
                             #'views/res_partner_view.xml',  # This file is used to create page 'tabs' with the attachments, not need if not wanted
                            ],
  "images"               :  ['static/description/fhs.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "pre_init_hook"        :  "pre_init_check",
}
