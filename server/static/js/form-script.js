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

                This is meant to clear the "invalid" input outlines
                when the user changes the values.
            */

            e.target.classList.remove('is-invalid');

            /*
                This is meant to remove the divs that contain
                error messages.
            */
            document.getElementById(`${e.target.id}-error`).remove();

        });

    });

});