// Need to call as website loads
window.onload = currentDate;

function addRowSearchContainer() {
  let table = document.getElementById("transfer_equivalency");

  let newRow = table.insertRow(-1);

  let cols = [
    `<div class="search-container">
            <input type="text" name="transfer_institution">
            <span class="search-icon" onclick="searchFunction()">🔍</span>
        </div>`,
    `<div class="search-container">
            <input type="text" name="subject_area">
            <span class="search-icon" onclick="searchFunction()">🔍</span>
        </div>`,
    `<div class="search-container">
            <input type="text" name="transfer_number">
            <span class="search-icon" onclick="searchFunction()">🔍</span>
        </div>`,
    `<input type="text" name="course_title">`,
    `<input type="text" name="uh_subject_area" value="UH Subject" readonly>`,
    `<input type="text" name="catalog_number" value="Catalog Nbr" readonly>`,
    `<input type="text" name="grade" value="Grade" readonly>`,
    `<input type="text" name="credits_transferred" value="0.000000" readonly>`,
    `<input type="text" name="credits_taken" value="0.00" readonly>`,
  ];

  cols.forEach((col, index) => {
    let cell = newRow.insertCell(index);
    cell.innerHTML = col;
  });
}

function deleteRowSearchContainer(button) {
  let row = button.parentNode.parentNode;
  let table = row.parentNode;
  if (table.rows.length > 2) {
    table.deleteRow(table.rows.length - 1);
  }
}

function addRowAttachmentBox() {
  let table = document.getElementById("attachment-box");

  let newRow = table.insertRow(-1);
  let cols = [
    `<td></td>`,
    `<td><input type="file" id="attachments" name="attachments" accept="image/*" /></td>`,
    `<td>
                <select id="file-description" name="file-description">
                <option value="" selected>Select...</option>
                <option value="optional_supplemental_document">Optional Supplemental Document</option>
                <option value="petition_course_syllabus">Petition Course Syllabus</option>
                <option value="petition_course_description">Petition Course Description</option>
                <option value="transfer_credit_summary">Transfer Credit Summary</option>
        </td>`,
    `<td></td>`,
    `<td><button onclick="deleteRowAttachmentBox(this)">Delete</button></td>`,
  ];

  cols.forEach((col, index) => {
    let cell = newRow.insertCell(index);
    cell.innerHTML = col;
  });
}

function deleteRowAttachmentBox(button) {
  let row = button.closest("tr");
  let table = document
    .getElementById("attachment-box")
    .getElementsByTagName("tbody")[0];

  if (table.rows.length > 1) {
    row.remove();
  }
}

function currentDate() {
  let myDate = new Date();
  let myMonth = myDate.getMonth() + 1;
  let myDay = myDate.getDate();
  let myYear = myDate.getFullYear();

  let todayDate = myMonth + "/" + myDay + "/" + myYear;

  document.getElementById("current_date").innerText = todayDate;
}

document
  .getElementById("signature")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = new Image();
        img.onload = function () {
          const canvas = document.getElementById("signatureCanvas");
          const ctx = canvas.getContext("2d");
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.src = e.target.result;
        document.getElementById("signatureCanvas").dataset.signature =
          e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });

document.getElementById("fill-out").addEventListener("click", function (e) {
  e.preventDefault();
  document.getElementById("uh_id").value = "12345678";
  document.getElementById("contact_phone").value = "(123) 456-7890";
  document.getElementById("transfer_institution").value = "Example University";
  document.getElementById("subject_area").value = "CS";
  document.getElementById("transfer_number").value = "101";
  document.getElementById("course_title").value =
    "Introduction to Computer Science";
  document.getElementById("uh_subject_area").value = "COSC";
  document.getElementById("catalog_number").value = "1301";
  document.getElementById("grade").value = "A";
  document.getElementById("credits_transferred").value = "3.0";
  document.getElementById("credits_taken").value = "3.0";
  document.getElementById("core_credit").value = "Yes";
  document.getElementById("core_area").value = "Math/Science";
  document.getElementById("course_credits").value = "3.0";
  document.getElementById("graduation_expected").checked = true;
  document.getElementById("course_prereq").checked = false;
  document.getElementById("major_requirement").checked = true;
  document.getElementById("minor_requirement").checked = false;
  document.getElementById("explanation").value =
    "Requesting credit transfer for equivalent coursework.";
});

function generateLaTeX() {
  let firstName = document.getElementById("first_name").value;
  let lastName = document.getElementById("last_name").value;
  let uhId = document.getElementById("uh_id").value;
  let contactPhone = document.getElementById("contact_phone").value;
  let transferInstitution = document.getElementById(
    "transfer_institution"
  ).value;
  let subjectArea = document.getElementById("subject_area").value;
  let transferNumber = document.getElementById("transfer_number").value;
  let courseTitle = document.getElementById("course_title").value;
  let coreCredit = document.getElementById("core_credit").value;
  let coreArea = document.getElementById("core_area").value;
  let courseCredits = document.getElementById("course_credits").value;
  let graduationExpected = document.getElementById("graduation_expected")
    .checked
    ? "Yes"
    : "No";
  let coursePrereq = document.getElementById("course_prereq").checked
    ? "Yes"
    : "No";
  let majorRequirement = document.getElementById("major_requirement").checked
    ? "Yes"
    : "No";
  let minorRequirement = document.getElementById("minor_requirement").checked
    ? "Yes"
    : "No";
  let explanation = document.getElementById("explanation").value;

  return `
  \\documentclass{article}
  \\usepackage{geometry}
  \\usepackage{graphicx}  % Ensure this is included
  \\geometry{margin=1in}
  \\begin{document}
  
  \\title{Undergraduate Student Credit Transfer Form}
  \\maketitle
  
  \\section*{Student Information}
  First Name: ${firstName} \\\\
  Last Name: ${lastName} \\\\
  UH ID: ${uhId} \\\\
  Contact Phone: ${contactPhone} \\\\
  
  \\section*{Transfer Equivalency}
  Transfer Institution: ${transferInstitution} \\\\
  Subject Area: ${subjectArea} \\\\
  Transfer Course Number: ${transferNumber} \\\\
  Course Title: ${courseTitle} \\\\
  
  \\section*{Transfer Credit Request}
  Core Credit: ${coreCredit} \\\\
  Core Area: ${coreArea} \\\\
  Course Credits: ${courseCredits} \\\\
  
  \\section*{Additional Information}
  Expected to Graduate in Next 12 Months: ${graduationExpected} \\\\
  PreReq for Upcoming Course Enrollment: ${coursePrereq} \\\\
  Requirement for Major: ${majorRequirement} \\\\
  Requirement for Minor: ${minorRequirement} \\\\
  
  \\section*{Explanation}
  ${explanation} \\\\
  
  \\section*{Signature Section}
  Student Signature: \\\\
  \\includegraphics[width=7cm]{signature.png}
  
  \\end{document}
  `;
}

function downloadLaTeX(content) {
  let blob = new Blob([content], { type: "text/plain" });
  let link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "credit_transfer_form.tex";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
// Generate LaTeX file from form data
document
  .getElementById("credit_transfer_form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    let texContent = generateLaTeX();
    const canvas = document.getElementById("signatureCanvas");
    const signatureBase64 = canvas.toDataURL("image/png");

    try {
      const response = await fetch("/update-latex", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          formName: "undergraduate transfer form",
          content: texContent,
          signature: signatureBase64,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert("Successfully submitted form");
      } else {
        console.error("Error saving file");
      }
    } catch (error) {
      console.error("Request failed", error);
    }
  });
