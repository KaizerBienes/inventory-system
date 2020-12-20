const backendUrl = 'http://127.0.0.1:5000';
const HTTP_NOT_ACCEPTABLE = 406;
const ENTER_KEY_PRESS = 13;

$(document).foundation();

$(document).ready(function() {
    let parseValidationError = function(errors) {
        let errorString = '';
        console.log(errors);
        for (const [key, value] of Object.entries(errors)) {
            errorString += `<p><b>${key.replace('_', ' ')}: </b>${value}</p>`
        };

        return errorString;
    };

    $("#create-inventory-form")
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

            axios.post(backendUrl + '/api/inventory', formData).then(function (response) {
                // successfully created inventory item
                location.href = "/";
            }).catch(function (error) {
                try {
                    $('#create-inventory-error-modal p').remove();
                    if (error.response.status == HTTP_NOT_ACCEPTABLE) { // validation errors
                        $('#create-inventory-error-modal')
                            .append($('<p>')
                            .append(parseValidationError(error.response.data.error.errors)));
                    } else if (error.response.data.error.message !== undefined) {
                        $('#create-inventory-error-modal')
                            .append($('<p>')
                            .append('<b>Error message: </b>' + error.response.data.error.message));
                    } else {
                        $('#create-inventory-error-modal')
                            .append($('<p>')
                            .append(error));
                    }
                } catch (e) {
                        $('#create-inventory-error-modal').show().append($('<p>').append(error));
                }

                $('#create-inventory-error-modal').foundation('open');
            });
        }).on("submit", function(event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            event.preventDefault();
            return false;
        });
});