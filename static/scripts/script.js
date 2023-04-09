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
  $('.sidenav').sidenav({
    draggable: 'true',
    inDuration: 250,
    outDuration: 250,
    preventScrolling: true
  });
  $('.dropdown-trigger').dropdown({
    inDuration: 300,
    outDuration: 225,
    constrain_width: false, // Does not change width of dropdown to that of the activator
    hover: false, // De-Activate on hover
    gutter: 0, // Spacing from edge
    belowOrigin: false, // Displays dropdown below the button
    alignment: 'left' // Displays dropdown with edge aligned to the left of button
  });
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