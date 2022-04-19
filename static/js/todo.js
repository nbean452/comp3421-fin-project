function validateForm() {
  var y, x;
  y = document.getElementById("taskName");
  x = document.getElementById("dueDate");

  if (y.value == "") {
    y.className += " invalid";
  }
  if (x.value == "") {
    x.className += " invalid";
  }
}


// $('table tbody tr').click(function () {
//   $(this).toggleClass('strikeout change');
//   var text = $(this).find('td:eq(2)').text();
//   if (text === "Not Finished") {
//     $(this).find('td:eq(2)').text('Finished');
//   } else {
//     $(this).find('td:eq(2)').text('Not Finished')
//   };



});
$(document).ready(function () {
  $('#dtBasicExample').DataTable();
  $('.dataTables_length').addClass('bs-select');
});

var closebtns = document.getElementsByClassName("close");
var i;
for (i = 0; i < closebtns.length; i++) {
  closebtns[i].addEventListener("click", function () {
    (this.parentElement).parentElement.style.display = 'none';
  });
}

function getDateFromString(str) {

  var dateParts = str.split('-');
  var date = new Date();

  date.setHours(0, 0, 0, 0);
  date.setDate(dateParts[0]);
  date.setMonth(dateParts[1] - 1);
  date.setFullYear(dateParts[2]);

  return date;
}

document.querySelectorAll('table td').forEach(function (td) {

  var today = new Date();
  today.setHours(0, 0, 0, 0);

  if (getDateFromString(td.innerText) < today) {

    td.parentElement.style.color = 'red';

  }
});

$("#calendar").fullCalendar({
  header: {
    left: 'prev',
    center: 'title',
    right: 'next'
  },

});

$('#calendarView').on('shown.bs.modal', function () {
  $("#calendar").fullCalendar('render');
});