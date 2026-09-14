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

// Figure viewer: click a research figure on a student page to see it enlarged.
// Opens fitted to the screen; click the image again for a larger, scrollable
// view. Backdrop click, the × button, or Escape closes it.
(function () {
  var figs = document.querySelectorAll('.research-figure img');
  if (!figs.length) return;

  var style = document.createElement('style');
  style.textContent =
    '.research-figure img{cursor:zoom-in;}' +
    '.fig-lb{position:fixed;inset:0;z-index:1000;background:rgba(12,14,18,.95);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:52px 12px 16px;box-sizing:border-box;cursor:zoom-out;}' +
    '.fig-lb[hidden]{display:none;}' +
    '.fig-lb-stage{max-width:100%;max-height:100%;overflow:auto;-webkit-overflow-scrolling:touch;}' +
    '.fig-lb-stage img{display:block;margin:auto;background:#fff;border-radius:6px;cursor:zoom-in;}' +
    '.fig-lb-stage.full img{cursor:zoom-out;}' +
    '.fig-lb-cap{margin:12px 0 0;max-width:900px;color:#e6e8ec;font:13px/1.5 system-ui,sans-serif;text-align:center;}' +
    '.fig-lb-close{position:absolute;top:10px;right:12px;width:40px;height:40px;border:0;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font:26px/40px system-ui,sans-serif;cursor:pointer;}' +
    '.fig-lb-close:hover{background:rgba(255,255,255,.26);}';
  document.head.appendChild(style);

  var box = document.createElement('div');
  box.className = 'fig-lb';
  box.hidden = true;
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Enlarged figure');
  box.innerHTML = '<button class="fig-lb-close" type="button" aria-label="Close">&times;</button>' +
    '<div class="fig-lb-stage"><img alt=""></div><p class="fig-lb-cap"></p>';
  document.body.appendChild(box);

  var stage = box.querySelector('.fig-lb-stage');
  var big = stage.querySelector('img');
  var cap = box.querySelector('.fig-lb-cap');
  var closeBtn = box.querySelector('.fig-lb-close');
  var opener = null;

  // Fitted: as large as the screen allows (small images scale up so text is
  // readable). Full: natural size, or twice the fitted size if that is larger.
  function size() {
    var nw = big.naturalWidth, nh = big.naturalHeight;
    if (!nw || !nh) return;
    var availW = window.innerWidth - 24;
    var availH = window.innerHeight - 52 - 16 - (cap.textContent ? cap.offsetHeight + 12 : 0);
    var fit = Math.min(availW / nw, availH / nh);
    var scale = stage.classList.contains('full') ? Math.max(1, fit * 2) : fit;
    big.style.width = Math.round(nw * scale) + 'px';
    big.style.height = Math.round(nh * scale) + 'px';
  }

  function open(img) {
    opener = img;
    var fc = img.closest('figure') && img.closest('figure').querySelector('figcaption');
    cap.textContent = fc ? fc.textContent.trim() : '';
    stage.classList.remove('full');
    big.alt = img.alt || '';
    big.onload = size;
    big.src = img.currentSrc || img.src;
    box.hidden = false;
    document.documentElement.style.overflow = 'hidden';
    size();
    closeBtn.focus();
  }

  function close() {
    box.hidden = true;
    document.documentElement.style.overflow = '';
    if (opener) opener.focus();
  }

  Array.prototype.forEach.call(figs, function (img) {
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.title = 'Click to enlarge';
    img.addEventListener('click', function () { open(img); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img); }
    });
  });

  box.addEventListener('click', function (e) {
    if (e.target === big) {
      stage.classList.toggle('full');
      size();
      stage.scrollTop = stage.scrollLeft = 0;
    } else {
      close();
    }
  });
  document.addEventListener('keydown', function (e) {
    if (!box.hidden && e.key === 'Escape') close();
  });
  window.addEventListener('resize', function () { if (!box.hidden) size(); });
})();
