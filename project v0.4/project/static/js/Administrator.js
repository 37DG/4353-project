// Logout function - Redirect to /auth/logout/
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

// Create User
function createUser() {
    const name = document.getElementById('createName').value;
    const email = document.getElementById('createEmail').value;
    const role = document.getElementById('createRole').value;
    const status = document.getElementById('createStatus').value;
    const level1 = document.getElementById('createLevel1').value;
    const level2 = document.getElementById('createLevel2').value;

    fetch('/create-user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, role, status, level1, level2 })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeModal('createModal');
        location.reload();
    });
}

// Update User
function updateUser() {
    const email = document.getElementById('updateEmail').value;
    const name = document.getElementById('updateName').value;
    const role = document.getElementById('updateRole').value;
    const status = document.getElementById('updateStatus').value;
    const level1 = document.getElementById('updateLevel1').value;
    const level2 = document.getElementById('updateLevel2').value;

    fetch('/update-user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, name, role, status, level1, level2 })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeModal('updateModal');
        location.reload();
    });
}

// Delete User
function deleteUser() {
    const name = document.getElementById('deleteName').value;
    const email = document.getElementById('deleteEmail').value;

    fetch('/delete-user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeModal('deleteModal');
        location.reload();
    });
}