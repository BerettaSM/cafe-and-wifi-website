function parseMessagesFromServer(messages) {
    /*
    This function takes in the server flashed messages
    as a string, and parses it to an array.
    Returns an array with each separate message,
    otherwise an empty array if there's no messages.
    */
    const parseRegex = /(&#39;|\[|\]|\')/gi;
    const result = messages.replaceAll(parseRegex, '');
    return result == '' ? [] : result.split(',').map(s => s.trim());
}

export function showServerMessages() {

    const title = 'Attention';

    const target = document.getElementById('server-messages');

    const message = target.innerText.trim();

    if(title === undefined || message === undefined || message.length == 0) return;

    const parsedMessages = parseMessagesFromServer(message);

    const messageModal = document.getElementById('message-modal');
    const modalTitle = document.getElementById('message-modal-label');
    const modalBody = document.getElementById('message-modal-body');

    modalTitle.innerText = title;

    const ul = document.createElement('ul');

    parsedMessages.forEach(message => {
        const liMessage = document.createElement('li');
        liMessage.innerText = message;
        liMessage.classList.add('fs-5');
        ul.appendChild(liMessage);
    });

    modalBody.innerHTML = null;
    modalBody.appendChild(ul);

    const messageModalInstance = new bootstrap.Modal(messageModal, {});
    messageModalInstance.show();

    target.innerHTML = null;

}

export function convertTimestampToElapsedTime(timestampString){

    /*
        timestampString should be formatted as: "2022-12-24 12:48:53"
    */

    const timestamp = new Date(timestampString.trim());

    const elapsedTime = new Date() - timestamp;

    const results = [
        [31536000, 'year', 'years'],
        [2628288, 'month', 'months'],
        [86400, 'day', 'days'],
        [3600, 'hour', 'hours'],
        [60, 'minute', 'minutes']
    ].reduce((arr, [divisor, singular, plural]) => {

        const result = Math.floor(elapsedTime / divisor / 1000);

        if(result > 0) {

            arr.push(`${result} ${result < 2 ? singular : plural} ago`)

        }

        return arr;

    }, [])

    return results.length === 0 ? 'Now' : results[0];

}
