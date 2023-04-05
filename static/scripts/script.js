// JQuery for Materialize library initializations
$(document).ready(function () {
  $(".dropdown-trigger").dropdown();
  $('.sidenav').sidenav();
  $('select').formSelect();
  // add active class for navigation menu items:
  let this_page = "{{ get_current_page() }}";
  let activeNavItem = NAV_ITEMS[this_page];
  // check if the current page has a navigation menu item:
  if (activeNavItem) {
    // if true add the active class to the navigation menu item:
    $('#' + activeNavItem).addClass('current');
  }
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