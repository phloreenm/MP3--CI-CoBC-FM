// Registration page password validation:
// Base Source Code: [Materialize Register Page Sample](https://codepen.io/HaldunA/pen/eJxRPG)

// Password field validation:
let pw1 = document.getElementById("password1"),
  pw2 = document.getElementById("password2");

function validatePassword() {
  if (pw1.value != pw2.value) {
    pw2.setCustomValidity("Passwords don't match");
  } else {
    pw2.setCustomValidity('');
  }
}
pw1.addEventListener("input", validatePassword);
pw2.addEventListener("input", validatePassword);

// Email field validation:
let email1 = document.getElementById("email1"),
  email2 = document.getElementById("email2");

function validateEmail() {
  console.log("validateEmail() called");
  console.log("email1.value:", email1.value);
  console.log("email2.value:", email2.value);
  if (email1.value != email2.value) {
    console.log("Emails don't match");
    email2.setCustomValidity("Emails don't match");
  } else {
    console.log("Emails match");
    email2.setCustomValidity('');
  }
}
email1.addEventListener("input", validateEmail);
email2.addEventListener("input", validateEmail);