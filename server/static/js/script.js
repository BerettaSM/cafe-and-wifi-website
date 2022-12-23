document.addEventListener('DOMContentLoaded', () => {

    const formValidationFieldIds = ['name', 'location','img_url', 'map_url', 'coffee_price'];

    formValidationFieldIds.forEach(fieldId => {

        const field = document.getElementById(fieldId);

        if(field !== null) {

            field.addEventListener('input', (e) => {

                /*
                    Validation is performed on the server side.

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

        }

    });

    const loginButton = document.getElementById('login-button');

    if(loginButton !== null) {

        /*
            Automatically closes the right-side
            menu when login modal is opened.
        */

        loginButton.addEventListener('click', e => {

            const offCanvas = document.getElementById('offcanvas-navbar');
            const openedOffCanvas = bootstrap.Offcanvas.getInstance(offCanvas);
            openedOffCanvas.hide();

        });

    }

    const deleteButton = document.getElementById('del-button');

    if(deleteButton !== null) {

        /*
            Confirmation button for delete cafe button.
        */

        deleteButton.addEventListener('click', (e) => {

            if(!window.confirm('Are you sure you want to delete?')) e.preventDefault();

        });

    }

});