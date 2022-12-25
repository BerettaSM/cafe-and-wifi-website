export function convertTimestampToElapsedTime(timestampString){

    /*
        timestampString should be formatted as: "2022-12-24 12:48:53" -> "year-month-day hour:minute:second"
    */

    const timestamp = new Date(timestampString.trim());

    const elapsedTime = new Date() - timestamp;

    const results = [
        [31536000, 'year', 'years'],
        [2628288, 'month', 'months'],
        [86400, 'day', 'days'],
        [3600, 'hour', 'hours'],
        [60, 'minute', 'minutes']
    ]
    .reduce((arr, [divisor, singular, plural]) => {

        const result = Math.floor(elapsedTime / divisor / 1000);

        if(result > 0) {

            arr.push(`${result} ${result < 2 ? singular : plural} ago`)

        }

        return arr;

    }, [])

    return results.length === 0 ? 'Now' : results[0];

}

function parseMessagesFromServer(messages) {

    /*
    This function takes in the server flashed messages
    as a string, and parses it to an array.
    Returns an array with each separate message,
    otherwise an empty array if there's no messages.
    */

    const replacedMessages =  [
        ["'", '"'],
        ['(', '['],
        [')', ']']
    ].reduce((messagesString, [from, to]) => {

        return messagesString.replaceAll(from, to);

    }, messages);

    return JSON.parse(replacedMessages);

}

export function showServerMessages() {

    const target = document.getElementById('server-messages');

    const messages = target.innerText.trim();

    if(messages === undefined || messages.length == 0) return;

    const parsedMessages = parseMessagesFromServer(messages);

    const messageModal = document.getElementById('message-modal');

    const modalTitle = document.getElementById('message-modal-label');

    const modalBody = document.getElementById('message-modal-body');

    modalTitle.innerText = "Server says:";

    const ul = document.createElement('ul');

    parsedMessages.forEach(([type, message]) => {

        const liMessage = document.createElement('li');

        liMessage.classList.add(`fs-5`);

        liMessage.innerText = message;

        ul.appendChild(liMessage);

    });

    modalBody.innerHTML = null;

    modalBody.appendChild(ul);

    const messageModalInstance = new bootstrap.Modal(messageModal, {});

    messageModalInstance.show();

    target.innerHTML = null;

}

export function triggerDeleteConfirmation(htmlElement) {

    /*
        This function triggers a delete confirmation.

        It takes the endpoint from an arbitrary attribute "data-confirm-url",
        expected to be contained inside the parameter "htmlElement", and triggers
        it by clicking the confirm button inside "modal_confirm.html".
        Finally, it triggers the modal window.
    */

    const confirmationModalElement = document.getElementById('confirmation-modal');

    if(confirmationModalElement === null || htmlElement === null || htmlElement === undefined) return;

    const endpoint = htmlElement.getAttribute('data-confirm-url');

    const modalHeader = confirmationModalElement.querySelector('h1.modal-title');

    const modalBody = confirmationModalElement.querySelector('div.modal-body');

    const confirmButton = confirmationModalElement.querySelector('button.confirm-button');

    const confirmAnchor = confirmationModalElement.querySelector('a.confirm-endpoint-url');

    modalHeader.innerText = 'Are you sure you want to delete?';

    modalBody.innerText = 'This action cannot be undone.';

    confirmButton.innerText = 'Delete';

    confirmButton.classList.remove('btn-primary');

    confirmButton.classList.add('btn-outline-danger');

    confirmAnchor.href = endpoint;

    const confirmationModalInstance = new bootstrap.Modal(confirmationModalElement, {});

    confirmationModalInstance.show();

}
