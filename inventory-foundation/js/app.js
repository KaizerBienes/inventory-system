const backendUrl = 'http://127.0.0.1:5000';
const HTTP_NOT_ACCEPTABLE = 406;
const ENTER_KEY_PRESS = 13;

$(document).foundation();

$(document).ready(function() {
    const queryString=window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const search_key = urlParams.get('search')

    if (search_key) {
        $('#search-inventory-text').val(search_key);
    }

    axios.get(backendUrl + '/api/inventory', {
            headers: {
                'Content-Type': 'application/json'
            },
            params: {
                'search': search_key
            }
        }).then(function (response) {
            let responseData = response.data;
            responseData.data.forEach(element => {
                $('#inventoryTableBody')
                    .append($('<tr>')
                        .append($('<td class="center-td">')
                            .append(
                                `<a id="update-inventory-button-${element.inventory.id}" class="button center-button">
                                    <i class="fi-pencil size-36"></i>
                                </a>`
                            ).append(
                                `<a id="delete-inventory-button-${element.inventory.id}" class="alert button center-button">
                                    <i class="fi-trash size-36"></i>
                                </a>`
                            ))
                        .append($('<td>').append(element.category.name))
                        .append($('<td>').append(element.inventory.item_number))
                        .append($('<td>').append(element.item_detail.item_name))
                        .append($('<td>').append(element.item_detail.description))
                        .append($('<td class="text-right">').append(`&#x20B1; ${element.inventory.cost_price.toFixed(2)}`))
                        .append($('<td class="text-right">').append(`${element.inventory.quantity} ${element.inventory.unit_abbreviation}`))
                    );
            });

        })
        .catch(function (error) {
            try {
                if (error.response.status == HTTP_NOT_ACCEPTABLE) { // validation errors
                    $('#error-bag').show().append($('<p>').append('Invalid request: ' + JSON.stringify(error.response.data.error.errors)));
                } else if (error.response.data.error.message !== undefined) {
                    $('#error-bag').show().append($('<p>').append('Message: ' + error.response.data.error.message));
                } else {
                    $('#error-bag').show().append($('<p>').append(error));
                }
            } catch (e) {
                    $('#error-bag').show().append($('<p>').append(error));
            }
        });

    handle_search_click = function () {
        window.location.href = window.location.pathname + "?" + $.param({
            'search': $('#search-inventory-text').val()
        });
    };
    $('#search-inventory-button').click(handle_search_click)

    $(document).on('keypress',function(e) {
        if(e.which == ENTER_KEY_PRESS) {
            handle_search_click()
        }
    });

    $(document).on('click', "a[id^='delete-inventory-button-']", function() {
        console.log("hit id!");
        let deleteButtonId = $(this).attr('id').replace('delete-inventory-button-', '');

        axios.delete(backendUrl + '/api/inventory/' + deleteButtonId, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function (response) {
            location.reload();
        }).catch(function (error) {
            console.log("error: " + error);
        });
    });

    $(document).on('click', "a[id^='update-inventory-button-']", function() {
        console.log("hit id!");
        window.location.href = window.location.origin + '/update-inventory.html' + "?" + $.param({
            'inventory_id': $(this).attr('id').replace('update-inventory-button-', '')
        });
    });
})
