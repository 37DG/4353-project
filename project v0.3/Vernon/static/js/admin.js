let currentApproveStatus = null;
function addRow() {
  let table = document.getElementById("userTable");
  let confirmCreateBtn = document.getElementById("confirm-create-btn");
  let createBtn = document.getElementById("create-btn");
  document.getElementById("update").disabled = true;
  createBtn.style.display = "none";
  confirmCreateBtn.style.display = "inline";
  let row = table.insertRow(-1);
  for (let i = 0; i < 2; i++) {
    let cell = row.insertCell(i);
    cell.contentEditable = "true";
  }
  let roleCell = row.insertCell(2);
  roleCell.innerHTML = `
  <select>
      <option value="admin">Admin</option>
      <option value="undergraduate-student" selected>undergraduate-student</option>
      <option value="graduate-student">graduate-student</option>
    </select>
    `;
  let statusCell = row.insertCell(3);
  statusCell.innerHTML = `
  <select>
      <option value="True" selected>Active</option>
      <option value="False">Deactivated</option>
  </select>
  `;
  let deleteCell = row.insertCell(4);
  deleteCell.innerHTML = '<button onclick="deleteRow(this)">Delete</button>';
}

function confirmAddRow() {
  let table = document.getElementById("userTable");
  let confirmCreateBtn = document.getElementById("confirm-create-btn");
  let createBtn = document.getElementById("create-btn");

  // Loop through each row (starting from 1 because the first row is header)
  for (let i = 1; i < table.rows.length; i++) {
    // Check if all fields are filled out
    let email = table.rows[i].cells[0].innerText.trim();
    let name = table.rows[i].cells[1].innerText.trim();
    let role = table.rows[i].cells[2].querySelector("select").value;
    let status = table.rows[i].cells[3].querySelector("select").value;

    if (!email || !name || !role || !status) {
      alert("Please fill in all fields.");
      return; // Exit the function if any field is empty
    }

    // Disable editing once fields are confirmed
    table.rows[i].cells[0].contentEditable = "false";
    table.rows[i].cells[1].contentEditable = "false";
    const dropDownEleRole = table.rows[i].cells[2].querySelector("select");
    const dropDownEleStatus = table.rows[i].cells[3].querySelector("select");

    if (dropDownEleRole) dropDownEleRole.disabled = true;
    if (dropDownEleStatus) dropDownEleStatus.disabled = true;

    // Call the addUser function to store the new user in the database
    if (i === table.rows.length - 1) addUser(email, name, role, status);
  }
  document.getElementById("update").disabled = false;
  createBtn.style.display = "inline";
  confirmCreateBtn.style.display = "none";
}

function addUser(email, name, role, status) {
  // Create the POST request to send data to the backend (Flask route)
  fetch("/add_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      name: name,
      role: role,
      account_status: status,
    }),
  })
    .then((response) => {
      if (response.ok) {
        alert("User added successfully!");
        location.reload(); // Reload the page to reflect changes
      } else {
        alert("Error adding user.");
      }
    })
    .catch((error) => {
      alert("Error: " + error);
    });
}

function deleteRow(button, email) {
  let row = button.parentNode.parentNode;
  row.parentNode.removeChild(row);
  deleteUser(email);
}

function enableEditing() {
  document.getElementById("update").style.display = "none";
  document.getElementById("confirm-update").style.display = "inline";
  document.getElementById("create-btn").disabled = true;
  let table = document.getElementById("userTable");
  for (let i = 1; i < table.rows.length; i++) {
    if (
      table.rows[i].cells[2].querySelector("select").value.toLowerCase() ===
      "admin"
    )
      continue;
    for (let j = 1; j < 4; j++) {
      table.rows[i].cells[j].contentEditable = "true";
      const dropDownEle = table.rows[i].cells[j].querySelector("select");
      if (dropDownEle) dropDownEle.disabled = false;
    }
  }
}
function confirmUpdate() {
  document.getElementById("update").style.display = "inline";
  document.getElementById("confirm-update").style.display = "none";

  let table = document.getElementById("userTable");
  let updatedUsers = [];
  for (let i = 1; i < table.rows.length; i++) {
    if (table.rows[i].cells[1].contentEditable === "true") {
      let email = table.rows[i].cells[0].innerText.trim();
      let name = table.rows[i].cells[1].innerText.trim();
      let role = table.rows[i].cells[2].querySelector("select").value;
      let account_status = table.rows[i].cells[3].querySelector("select").value;
      updatedUsers.push({ email, name, role, account_status });

      for (let j = 0; j < 4; j++) {
        table.rows[i].cells[j].contentEditable = "false";
        const dropDownEle = table.rows[i].cells[j].querySelector("select");
        if (dropDownEle) dropDownEle.disabled = true;
      }
    }
  }
  if (updatedUsers.length > 0) {
    fetch("/update_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ users: updatedUsers }),
    })
      .then((response) => {
        if (response.ok) {
          alert("User(s) updated successfully!");

          location.reload(); // Reload the page to reflect changes
        } else {
          alert("Error updating user(s).");
        }
      })
      .catch((error) => {
        alert("Error: " + error);
      });
  }
  document.getElementById("create-btn").disabled = false;
}

function deleteUser(email) {
  // Confirm before sending the delete request
  if (confirm("Are you sure you want to delete this user?")) {
    fetch("/delete_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email, // Email of the user to be deleted
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response after deletion
        if (data.message === "User deleted") {
          alert("User has been deleted successfully!");
          // Optionally, remove the user row from the table if needed
          document.getElementById("user-" + email).remove();
        } else {
          alert("Failed to delete user.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

function viewForm(formId, userEmail) {
  event.preventDefault();
  fetch("/show_pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ formId, userEmail }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      const url = URL.createObjectURL(blob);
      window.open(url);
    })
    .catch((error) => {
      console.log("Error: ", error);
    });
}

let currentFormId = null;
document
  .getElementById("approver-signature")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = new Image();
        img.onload = function () {
          const canvas = document.getElementById("approver-signature-canvas");
          const ctx = canvas.getContext("2d");
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.src = e.target.result;
        document.getElementById("approver-signature-canvas").dataset.signature =
          e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
function openApprovalModal(formId, approve) {
  currentFormId = formId;
  const modal = document.getElementById("approval-modal");
  const modalContent = modal.querySelector(".modal-content");

  // Show the modal
  modal.style.display = "block";

  // Change modal content based on approve flag
  if (approve) {
    // Approve case
    modalContent.querySelector("h2").textContent = "Approve Form";
    modalContent.querySelector("p").textContent =
      "Upload your signature to approve the form.";
    modalContent.querySelector("button").textContent = "Submit Approval";
    currentApproveStatus = "approved";
  } else {
    // Deny case
    modalContent.querySelector("h2").textContent = "Deny Form";
    modalContent.querySelector("p").textContent =
      "Are you sure you want to deny this form?";
    modalContent.querySelector("button").textContent = "Submit Denial";
    currentApproveStatus = "denied";
  }
}

function openDenyModal(formId) {
  currentFormId = formId;
}

function closeModal() {
  document.getElementById("approval-modal").style.display = "none";
}

document
  .getElementById("approval-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const canvas = document.getElementById("approver-signature-canvas");
    const approverSignatureBase64 = canvas.toDataURL("image/png");
    if (approverSignatureBase64.length === 0) {
      alert("Please upload your signature.");
      return;
    }
    const status = currentApproveStatus === "approved" ? "approved" : "denied";
    try {
      const response = await fetch("/approve-deny-form", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          approverSignatureBase64,
          formId: currentFormId,
          status,
        }),
      });

      if (response.ok) {
        alert("Form approved successfully!");
        closeModal();
        location.reload();
      } else {
        console.error("Approval failed");
        alert("Failed to approve form.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });

document.querySelectorAll(".request-info-btn").forEach((button) => {
  button.addEventListener("click", (event) => {
    const returnedFormId = event.target.id;
    document.getElementById("request-info-modal").style.display = "block";
    document.getElementsByClassName("request-info-btn").disabled = true; // Disable the button after clicking
    document.getElementById("request-info-modal").dataset.formId =
      returnedFormId;
  });
});

// Close the "Request More Info" modal
function closeRequestInfoModal() {
  document.getElementById("request-info-modal").style.display = "none";
}

async function submitRequestInfo() {
  const returnedFormId =
    document.getElementById("request-info-modal").dataset.formId;
  const comment = document.getElementById("request-info-reason").value;

  if (!comment) {
    alert("Please provide a reason.");
    return;
  }

  try {
    const response = await fetch("/return-form", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        returnedFormId,
        comment,
      }),
    });

    if (response.ok) {
      const result = await response.json();
      alert("Successfully return form to request more info");
      location.reload();
    } else {
      console.error("Error return file to request more info");
    }
  } catch (error) {
    console.error("Request failed - return file to request more info", error);
  }
}
