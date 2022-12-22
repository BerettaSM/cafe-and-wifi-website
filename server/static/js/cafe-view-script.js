document.addEventListener('DOMContentLoaded', () => {

    const deleteButton = document.getElementById('del-button');

    deleteButton.addEventListener('click', (e) => {

        if(!window.confirm('Are you sure you want to delete?')) e.preventDefault();

    });

});
