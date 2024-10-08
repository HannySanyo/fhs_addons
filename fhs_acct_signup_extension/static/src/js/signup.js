//////////////////////////////////////////////////////////////////////////////////
// File Name: __inti__.py
// Revision History:  Engineer    Date          Description
//                    G. Sanyo    10/08/2024    Add compnay name and address fields
//                    G. Sanyo    09/29/2024    Creation
//////////////////////////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function () {
    const companyNameInput = document.getElementById('company_name');
    const companyAddressDiv = document.getElementById('company_address');

    companyNameInput.addEventListener('input', function () {
        if (this.value) {
            companyAddressDiv.style.display = 'block';
        } else {
            companyAddressDiv.style.display = 'none';
        }
    });
});
