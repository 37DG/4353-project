// Function to generate a random string of given length
function getRandomString(length) {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function getRandomCareer() {
  const careers = ["Graduate", "Law", "Optometry", "Pharmacy"];
  return careers[Math.floor(Math.random() * careers.length)];
}

function getRandomFiveDigitNumber() {
  return Math.floor(10000 + Math.random() * 90000);
}

function getRandomDate(startYear, endYear) {
  const start = new Date(startYear, 0, 1);
  const end = new Date(endYear, 11, 31);
  return new Date(
    start.getTime() + Math.random() * (end.getTime() - start.getTime())
  );
}

function getRandomPhoneNumber() {
  const areaCode = Math.floor(100 + Math.random() * 900);
  const centralOfficeCode = Math.floor(100 + Math.random() * 900);
  const lineNumber = Math.floor(1000 + Math.random() * 9000);
  return `(${areaCode}) ${centralOfficeCode}-${lineNumber}`;
}

function fillOutForm() {
  document.getElementById("uh_id").value = getRandomFiveDigitNumber();
  document.querySelector('input[type="tel"][required]').value =
    getRandomPhoneNumber();
  document.querySelector("#program").value = [
    "ARCH",
    "ARTS",
    "BUSI",
    "EDUC",
    "ENGR",
    "HPA",
    "HRM",
    "LAW",
    "LASS",
    "NSM",
    "NURS",
    "OPTO",
    "PHAR",
    "SOCW",
    "TECH",
  ][Math.floor(Math.random() * 15)];
  document.getElementById("career").value = "Law";

  document.getElementById("effective_term").value = [
    "Spring",
    "Fall",
    "Summer",
  ][Math.floor(Math.random() * 3)]; // Effective Term
  document.getElementById("year").value = Math.floor(2023 + Math.random() * 8);
  document.querySelector("#update_program").checked = Math.random() > 0.5;
  document.querySelector("#admissions_status").checked = Math.random() > 0.5;
  document.querySelector("#add_new_concurrent").checked = Math.random() > 0.5;
  document.querySelector("#change_degree_objective").checked =
    Math.random() > 0.5;
  document.querySelector("#degree_requirement_exception").checked =
    Math.random() > 0.5;
  document.querySelector("#leave_of_absence").checked = Math.random() > 0.5;
  document.querySelector("#reinstatement").checked = Math.random() > 0.5;
  document.querySelector("#late_filing_graduation").checked =
    Math.random() > 0.5;
  document.querySelector("#transfer_credit").checked = Math.random() > 0.5;
  document.querySelector("#change_admit_term").checked = Math.random() > 0.5;
  document.querySelector("#early_submission").checked = Math.random() > 0.5;
  document.querySelector("#other").checked = Math.random() > 0.5;

  if (document.querySelector("#leave_of_absence").checked) {
    document.querySelector(".sub-item input").value =
      "Supporting documentation goes here";
  }

  document.querySelector('textarea[rows="5"]').value =
    "This is a random explanation for the petition request.";
}

document.getElementById("fill-out").addEventListener("click", function (event) {
  event.preventDefault();
  fillOutForm();
});

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

document
  .getElementById("petitionForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {};

    formData.forEach((value, key) => {
      data[key] = value;
    });

    const canvas = document.getElementById("signatureCanvas");
    const signatureBase64 = canvas.toDataURL("image/png"); //
    let latexContent = `
    \\documentclass[a4paper,12pt]{article}
    \\usepackage{geometry}
    \\geometry{top=1in, bottom=1in, left=1in, right=1in}
    \\usepackage{longtable}
    \\usepackage{amsmath}
    \\usepackage{graphicx}
    
    \\title{Graduate Student Petition Form}
    \\author{University of Houston}
    \\date{}
    
    \\begin{document}
    
    \\maketitle
    
    \\section*{Student Information}
    \\begin{tabbing}
    First Name: \\hspace{3cm} \\= \\underline{\\hspace{5cm} ${
      data["first_name"]
    }} \\\\
    Middle Name: \\> \\underline{\\hspace{5cm} ${data["middle_name"]}} \\\\
    Last Name: \\> \\underline{\\hspace{5cm} ${data["last_name"]}} \\\\
    UH ID: \\> \\underline{\\hspace{5cm} ${data["uh_id"]}} \\\\
    Contact Phone: \\> \\underline{\\hspace{5cm} ${data["contact_phone"]}} \\\\
    \\end{tabbing}
    
    \\section*{Current Student Information}
    \\begin{tabbing}
    Program: \\hspace{3cm} \\= \\underline{\\hspace{5cm} ${
      data["program"]
    }} \\\\
    Career: \\> \\underline{\\hspace{5cm} ${data["career"]}} \\\\
    \\end{tabbing}
    
    \\section*{Petition Effective}
    \\begin{tabbing}
    Effective Term: \\hspace{2cm} \\= \\underline{\\hspace{5cm} ${
      data["effective_term"]
    }} \\\\
    Year: \\> \\underline{\\hspace{5cm} ${data["year"]}} \\\\
    \\end{tabbing}
    
    \\section*{Purpose of Petition}
    \\begin{enumerate}
        \\item Update programs status/action (term activate, discontinue, etc) \\hfill [${
          data["update_program"] ? "yes" : "no"
        }]
        \\item Admissions status change (e.g. conditional to unconditional) \\hfill [${
          data["admissions_status"] ? "yes" : "no"
        }]
        \\item Add new concurrent degree or certificate objective (career/program/plan) \\hfill [${
          data["add_new_concurrent"] ? "yes" : "no"
        }]
        \\item Change current degree objective (program/plan) \\hfill [${
          data["change_degree_objective"] ? "yes" : "no"
        }]
        \\item Degree requirement exception or approved course substitution \\hfill [${
          data["degree_requirement_exception"] ? "yes" : "no"
        }]
        \\item Leave of Absence (include specific term) \\hfill [${
          data["leave_of_absence"] ? "yes" : "no"
        }]
        \\item Reinstatement to discontinued Career (provide explanation) \\hfill [${
          data["reinstatement"] ? "yes" : "no"
        }]
        \\item Request to apply to graduate after the late filing period deadline \\hfill [${
          data["late_filing_graduation"]
        }]
        \\item Transfer Credit \\hfill [${
          data["transfer_credit"] ? "yes" : "no"
        }]
        \\item Change Admit Term \\hfill [${
          data["change_admit_term"] ? "yes" : "no"
        }]
        \\item Early Submission of Thesis/Dissertation \\hfill [${
          data["early_submission"] ? "yes" : "no"
        }]
        \\item Other (explain below) \\hfill [${data["other"] ? "yes" : "no"}]
    \\end{enumerate}
    
    \\section*{Explanation of Request}
    \\begin{flushleft}
    \\underline{\\hspace{15cm} ${data["explanation"]}} \\\\
    \\end{flushleft}
    
    \\section*{Signature Section}
    Student Signature: \\\\
    \\includegraphics[width=7cm]{signature.png}
    
    \\end{document}
    `;

    try {
      const response = await fetch("/update-latex", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          formName: "graduate student petition form",
          content: latexContent,
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
