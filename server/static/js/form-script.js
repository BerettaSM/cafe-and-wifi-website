document.addEventListener('DOMContentLoaded', () => {

    [
        document.getElementById('name'),
        document.getElementById('location'),
        document.getElementById('img_url'),
        document.getElementById('map_url'),
        document.getElementById('coffee_price')
    ]
    .forEach(field => {

        field.addEventListener('input', (e) => {

            /*
                Validation is performed server side.
                This is meant to just clear the "invalid" inputs
                when the user changes the values.
            */

            e.target.classList.remove('is-invalid');

            document.getElementById(`${e.target.id}-error`).remove();

        });

    });

});