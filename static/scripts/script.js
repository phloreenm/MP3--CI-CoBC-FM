const NAV_ITEMS = {
  'index': 'home',
  'procedures': 'procedures',
  'tasks': 'tasks',
  'login': 'login',
  'admin': 'dashboard',
  'employee': 'dashboard',
  'manager': 'dashboard',
  'users': 'users',
  'register': 'register',
};
// JQuery for Materialize library initializations
$(document).ready(function () {
  $(".dropdown-trigger").dropdown();
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.modal').modal();

  // add active class for navigation menu items:
  let this_page = window.location.pathname.split("/").pop();
  // check if the current page is in NAV_ITEMS
  if (NAV_ITEMS.hasOwnProperty(this_page)) {
    let activeNavItem = NAV_ITEMS[this_page];
    if (activeNavItem) {
      // if true add the active class to the navigation menu item:
      $('#' + activeNavItem).addClass('current');
    }
  } 
})

// remove Flash messages after the set timeout if flash_msg ID exists on page:
let flashMsg_exists = document.getElementById('flash_msg');
if (flashMsg_exists) {
  $(document).ready(function () {
    setTimeout(function () {
      $('#flash_msg').fadeOut('fast', function () {
        $(this).remove();
      });
    }, 5000)
  });
}