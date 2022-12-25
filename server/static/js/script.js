import { convertTimestampToElapsedTime, triggerDeleteConfirmation } from './lib.js';

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

                const errorSection = document.getElementById(`${e.target.id}-error`);

                if(errorSection !== null) errorSection.remove();

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

                triggerDeleteConfirmation(e.target);

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

        }, 60000);

        updateElapsedTime();

    }

    const yearSpan = document.getElementById('current-year');

    if(yearSpan !== null) {

        const currentYear = new Date().getFullYear();

        yearSpan.innerText = currentYear;

    }

});