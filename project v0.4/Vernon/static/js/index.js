function reactivateAccount() {
  const userEmail = "{{ user.email }}";

  fetch("/reactivate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email: userEmail }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Your account has been reactivated.");
        location.reload();
      } else {
        alert("Error reactivating the account.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred.");
    });
}

document
  .getElementById("graduate-petition-form")
  .addEventListener("click", () => {
    document
      .getElementById("graduate-petition-form-container")
      .classList.remove("hidden");
    document
      .getElementById("undergraduate-transfer-form-container")
      .classList.add("hidden");
  });

document
  .getElementById("undergraduate-transfer-form")
  .addEventListener("click", () => {
    document
      .getElementById("graduate-petition-form-container")
      .classList.add("hidden");
    document
      .getElementById("undergraduate-transfer-form-container")
      .classList.remove("hidden");
  });
1;
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
