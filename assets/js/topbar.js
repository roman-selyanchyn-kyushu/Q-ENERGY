// Mobile hamburger: toggles the section nav (.landing-nav#site-nav) open as a
// dropdown panel. Shared by index + news + activities + publications.
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (!btn || !nav) return;

  function close() {
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  }
  function toggle() {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    toggle();
  });
  // Close after a link tap, on outside click, or Escape.
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) close();
  });
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('open') && !nav.contains(e.target) && e.target !== btn) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });
})();
