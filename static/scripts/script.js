// JQuery for Materialize library initializations
$(document).ready(function () {
  $(".dropdown-trigger").dropdown();
  $('.sidenav').sidenav();
  $('select').formSelect();
})

// remove Flash messages after the set timeout if flash_msg ID exists on page:
let flashMsg_exists = document.getElementById('flash_msg');
if (flashMsg_exists) {
  $(document).ready(function() {
    console.log('Inside the document ready function');
    setTimeout(function() {
      console.log('Inside the setTimeout function')
      $('#flash_msg').fadeOut('fast', function() {
        console.log('Inside the fadeOut function')
        console.log('Nefore the remove function')
        $(this).remove();
        console.log('After the remove function')
      });
    }, 5000)
  });
}