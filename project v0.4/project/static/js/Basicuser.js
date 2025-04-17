function logoutUser() {
    window.location.href = "/auth/logout/";
}


// Open Modal
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// Close Modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';

    // Clear inputs when modal is closed
    const inputs = document.querySelectorAll(`#${modalId} input, #${modalId} select`);
    inputs.forEach(input => input.value = "");
}

function changeUsername() {
    const name = document.getElementById('changeName').value;

    fetch('/changeUsername/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeModal('ChangeUsernameModal');
        location.reload();
    });
}