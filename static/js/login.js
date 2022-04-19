function showPassword() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function validateForm() {
  var y, x;
  y = document.getElementById("username");
  x = document.getElementById("password");

  if (y.value == "") {
    y.className += " invalid";
  }
  if (x.value == "") {
    x.className += " invalid";
  }
}