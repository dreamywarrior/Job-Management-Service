// =============================
// Validation Helper Functions
// =============================

function showError(input, message) {

    input.classList.add("is-invalid");

    let feedback = input.nextElementSibling;

    if (!feedback || !feedback.classList.contains("invalid-feedback")) {

        feedback = document.createElement("div");
        feedback.className = "invalid-feedback";
        input.parentNode.appendChild(feedback);

    }

    feedback.innerText = message;
}

function clearError(input) {

    input.classList.remove("is-invalid");

    const feedback = input.parentNode.querySelector(".invalid-feedback");

    if (feedback)
        feedback.remove();

}

function validateRequired(input, fieldName){

    if(input.value.trim()===""){

        showError(input, fieldName+" is required.");

        return false;

    }

    clearError(input);

    return true;

}

function validateMinLength(input,min){

    if(input.value.trim().length<min){

        showError(

            input,

            "Minimum "+min+" characters required."

        );

        return false;

    }

    clearError(input);

    return true;

}

function validateEmail(input){

    const regex=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(!regex.test(input.value.trim())){

        showError(

            input,

            "Enter a valid email."

        );

        return false;

    }

    clearError(input);

    return true;

}

function validatePasswordMatch(password, confirm){

    if(password.value!==confirm.value){

    showError(
    confirm,
    "Passwords do not match."
    );

    return false;

    }

    clearError(confirm);

    return true;

    }

    function validateSalary(input){

    if(input.value===""){

    clearError(input);

    return true;

}

    const regex=/^[A-Za-z0-9 .-]+$/;

    if(!regex.test(input.value)){

    showError(
    input,
    "Invalid salary format."
    );

    return false;

    }

    clearError(input);

    return true;

}

function disableSubmit(button){

    button.disabled=true;

    button.innerHTML=`
    <span
    class="spinner-border spinner-border-sm">
    </span>

    Saving...
    `;

}

function validatePassword(input){

    const password = input.value;

    // At least:
    // 8 characters
    // 1 uppercase
    // 1 lowercase
    // 1 number
    // 1 special character

    const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()_+\-=\[\]{};':"\\|,.<>\/~`])[A-Za-z\d@$!%*?&^#()_+\-=\[\]{};':"\\|,.<>\/~`]{8,}$/;

    if(!regex.test(password)){

        showError(
            input,
            "Password must be at least 8 characters and contain an uppercase letter, lowercase letter, number, and special character."
        );

        return false;

    }

    clearError(input);

    return true;

}