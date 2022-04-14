function validateForm() {
    var  y, x;
    y = document.getElementById("taskName"); 
    x = document.getElementById("dueDate");    
    
    if (y.value == "") {
        y.className += " invalid";    
    }
    if (x.value == "") {
        x.className += " invalid";
    }
}


$('table tbody td').click(function() {
    $(this).parent().toggleClass( 'strikeout change' );
    
    
    
});
$(document).ready(function () {
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');
  });

var closebtns = document.getElementsByClassName("close");
var i;
for (i = 0; i < closebtns.length; i++) {
  closebtns[i].addEventListener("click", function() {
    (this.parentElement).parentElement.style.display = 'none';
  });
}