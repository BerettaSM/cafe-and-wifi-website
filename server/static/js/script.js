import { convertTimestampToElapsedTime } from './lib.js';

document.addEventListener('DOMContentLoaded', () => {

    const formValidationFieldIds = [
        'name',
        'location',
        'img_url',
        'map_url',
        'coffee_price',
        'signup_email',
        'signup_username',
        'signup_password',
        'signup_confirm'
    ];

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

    const deleteButtons = document.querySelectorAll('.del-button');

    if(deleteButtons !== null) {

        /*
            Confirmation message for delete buttons.
        */

        deleteButtons.forEach(button => {

            button.addEventListener('click', (e) => {

                if(!window.confirm('Are you sure you want to delete?')) e.preventDefault();

            });

        })

    }

    const comments = document.querySelectorAll('div.comment');

    if(comments !== null) {

        function updateElapsedTime() {

            comments.forEach(comment => {

                const timestampString = comment.querySelector('div.timestamp').innerText;

                const elapsedTime = convertTimestampToElapsedTime(timestampString);

                const target = comment.querySelector('small.elapsed-time');

                target.innerText = elapsedTime;

            });

        }

        setInterval(() => {

            updateElapsedTime();

        }, 1000);

        updateElapsedTime();

    }

});