const backendUrl = 'http://127.0.0.1:5000';
const HTTP_NOT_ACCEPTABLE = 406;
const ENTER_KEY_PRESS = 13;

$(document).foundation();

$(document).ready(function() {
    const queryString=window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const inventory_id = urlParams.get('inventory_id');

    let parseValidationError = function(errors) {
        let errorString = '';
        console.log(errors);
        for (const [key, value] of Object.entries(errors)) {
            errorString += `<p><b>${key.replace('_', ' ')}: </b>${value}</p>`
        };

        return errorString;
    };

    if (inventory_id == undefined) {
        $('#update-inventory-id-error-modal').foundation('open');
    } else {
        axios.get(`${backendUrl}/api/inventory/${inventory_id}`)
            .then(function (response) {
                // set values based from the response
                let responseData = response.data.data;
                $('#form-inventory-id').val(responseData.inventory.id);
                $('#form-category-name').val(responseData.category.name);
                $('#form-item-number').val(responseData.inventory.item_number);
                $('#form-item-name').val(responseData.item_detail.item_name);
                $('#form-description').val(responseData.item_detail.description);
                $('#form-cost-price').val(responseData.inventory.cost_price);
                $('#form-quantity').val(responseData.inventory.quantity);
                $('#form-unit-abbreviation').val(responseData.inventory.unit_abbreviation);
            }).catch(function (error) {
                try {
                    if (error.response.status == HTTP_NOT_ACCEPTABLE) { // validation errors
                        $('#update-inventory-id-error-modal h4')
                            .after($('<p>')
                                .append(parseValidationError(error.response.data.error.errors)));
                    } else if (error.response.data.error.message !== undefined) {
                        $('#update-inventory-id-error-modal h4')
                            .after($('<p>')
                                .append('Message: ' + error.response.data.error.message));
                    } else {
                        $('#update-inventory-id-error-modal h4')
                            .after($('<p>')
                                .append(error));
                    }
                } catch (e) {
                        $('#update-inventory-id-error-modal h4')
                            .after($('<p>')
                                .append(error));
                }

                $('#update-inventory-id-error-modal').foundation('open');
            });
    }

    $("#update-inventory-form")
        .on("forminvalid.zf.abide", function(event,el) {
            // let form validation generate errors
        })
        .on("formvalid.zf.abide", function(event,frm) {
            let elements = frm[0].elements;
            var formData = new FormData();
            for (var i=0; i < elements.length; i++) {
                var item = elements[i];
                formData.append(item.id.replace('form-', '').replace('-', '_'), item.value);
            }

            inventoryId = $('#form-inventory-id').val();
            axios.put(`${backendUrl}/api/inventory/${inventoryId}`, formData)
                .then(function (response) {
                    console.log(response);
                    // successfully updated inventory item
                    location.href = "/";
                }).catch(function (error) {
                    try {
                        $('#update-inventory-error-modal p').remove();
                        if (error.response.status == HTTP_NOT_ACCEPTABLE) { // validation errors
                            $('#update-inventory-error-modal')
                                .show()
                                .append($('<p>')
                                .append(parseValidationError(error.response.data.error.errors)));
                        } else if (error.response.data.error.message !== undefined) {
                            $('#update-inventory-error-modal')
                                .show()
                                .append($('<p>')
                                .append('<b>Error message: </b>' + error.response.data.error.message));
                        } else {
                            $('#update-inventory-error-modal')
                                .show()
                                .append($('<p>')
                                .append(error));
                        }
                    } catch (e) {
                        $('#update-inventory-error-modal').show().append($('<p>').append(error));
                    }

                    $('#update-inventory-error-modal').foundation('open');
                });
        }).on("submit", function(event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            event.preventDefault();
            return false;
        });
});