document.addEventListener("DOMContentLoaded", function() {
    let step1Select = document.getElementById("step1_option");
    let dropCoursesField = document.getElementById("dropCoursesField");
    let courseInputs = document.querySelectorAll("#dropCoursesField input");

    let step3Select = document.getElementById("step3_option");
    let returnDateField = document.getElementById("returnDateField");
    let returnDateInput = document.getElementById("return_date");

    // Show course input fields only if "keep_some" is selected
    step1Select.addEventListener("change", function() {
        if (step1Select.value === '2') {
            dropCoursesField.classList.remove("hidden");
        } else {
            dropCoursesField.classList.add("hidden");
            courseInputs.forEach(input => {
                input.value = "";});
        }
    });

    step3Select.addEventListener("change", function() {
        if (step3Select.value === '1') {
            returnDateField.classList.remove("hidden");
        } else {
            returnDateField.classList.add("hidden");
            returnDateInput.value = "";
        }
    });
});

function submitForm(actionUrl) {
    let Id = document.getElementById("id").value.trim();
    let step1_option = document.getElementById("step1_option").value;
    let departure_date = document.getElementById("departure_date").value;
    let step2_option = document.getElementById("step2_option").value;
    let step3_option = document.getElementById("step3_option").value;
    let return_date = document.getElementById("return_date").value;
    let step4_option1 = document.getElementById("step4_option1").checked;
    let step4_option2 = document.getElementById("step4_option2").checked;
    let step4_option3 = document.getElementById("step4_option3").checked;
    let step5_option1 = document.getElementById("step5_option1").checked;
    let step5_option2 = document.getElementById("step5_option2").checked;
    let step5_option3 = document.getElementById("step5_option3").checked;
    let step5_option4 = document.getElementById("step5_option4").checked;
    let step5_option5 = document.getElementById("step5_option5").checked;
    let step5_option6 = document.getElementById("step5_option6").checked;
    let step5_option7 = document.getElementById("step5_option7").checked;
    let signature = document.getElementById("signature").files.length;

    if (Id === "") {
        alert("ID is required.");
        return;
    }
    if (step1_option === "") {
        alert("Please select a departure plan in Step 1.");
        return;
    }
    if (step1_option === "2") {
        let drop_course1 = document.getElementById("drop_course1").value.trim();
        let drop_course2 = document.getElementById("drop_course2").value.trim();
        let drop_course3 = document.getElementById("drop_course3").value.trim();
        
        if (drop_course1 === "" && drop_course2 === "" && drop_course3 === "") {
            alert("You must enter at least one course if you select to keep some courses.");
            return;
        }
    }
    // Validate Step 2: Departure Date
    if (departure_date === "") {
        alert("Please select your departure date.");
        return;
    }

    // Validate Step 2: Departure Method
    if (step2_option === "") {
        alert("Please select how you will depart.");
        return;
    }
    if (step3_option === "") {
        alert("Please select a return plan in Step 3.");
        return;
    }
    if (!step4_option1 || !step4_option2 || !step4_option3) {
        alert("You must check all acknowledgements in Step 4.");
        return;
    }
    if (!step5_option1 || !step5_option2 || !step5_option3 || !step5_option4 || !step5_option5|| !step5_option6|| !step5_option7) {
        alert("You must check all responsibilities in Step 5.");
        return;
    }
    if (signature === 0) {
        alert("Please upload your signature.");
        return;
    }

    let form = document.getElementById("EarlyWithdrawForm");
    form.action = actionUrl;
    form.submit();
}