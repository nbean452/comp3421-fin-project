function showPassword(id) {
    var x = document.getElementById(id);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
  }
function checkpsw() {
    if (document.getElementById('psw').value ==
        document.getElementById('pswConfirm').value) {
        document.getElementById('message').style.display = 'none';
        document.getElementById('pswConfirm').className = "form-control";
        return true;
    } else {
        document.getElementById('message').style.display = 'inline';
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'Incorrect Password';
        document.getElementById('pswConfirm').className += " invalid";
        return false;
    }
}

var currentTab = 0; 
showTab(currentTab); 
  
function showTab(n) {
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }

    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
   
    fixStepIndicator(n)
}
  
function nextPrev(n) {
    var x = document.getElementsByClassName("tab");
    if (n == 1 && !validateForm()) return false;
    if ((currentTab == (x.length-1)) && !checkpsw()) return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    if (currentTab >= x.length) {
        document.getElementById("reg").submit();
        return false;
    }
    showTab(currentTab);
}
  
function validateForm() {
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    for (i = 0; i < y.length; i++) {
        if (y[i].value == "") {
            y[i].className += " invalid";
            valid = false;
        }
    }
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid;
}
  
function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}

  