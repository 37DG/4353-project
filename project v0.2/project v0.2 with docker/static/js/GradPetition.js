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
  
function submitForm(actionUrl) {
    // Normally we would validate inputs here but merged code doesn't
    let form = document.getElementById("petitionForm");
    form.action = actionUrl;
    form.submit();
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
  