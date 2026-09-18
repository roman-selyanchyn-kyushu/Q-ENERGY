// Site-wide language switch — the one implementation every page uses.
// Markup: <button class="lang-switch"> with a globe icon and two labels
// (.to-ja "日本語" / .to-en "English"); CSS shows the label for the *other*
// language, so a click always means "switch to that one".
// Loaded in <head> so a saved preference applies before first paint.
// Pages that need to react (e.g. activities captions) listen for 'langchange'.
(function () {
  var KEY = 'k2spring_lang';
  var root = document.documentElement;

  // Older pages stored 'jp'; normalise to the html lang value 'ja'.
  function norm(v) { return v === 'ja' || v === 'jp' ? 'ja' : v === 'en' ? 'en' : null; }

  function apply(lang, save) {
    root.lang = lang;
    // Landing-page text nodes that carry both strings (data-ja / data-en).
    document.querySelectorAll('[data-ja][data-en]').forEach(function (el) {
      el.textContent = el.dataset[lang];
    });
    document.querySelectorAll('.lang-switch').forEach(function (b) {
      b.setAttribute('aria-label', lang === 'ja' ? 'Switch to English' : '日本語に切り替え');
    });
    if (save) { try { localStorage.setItem(KEY, lang); } catch (e) {} }
    document.dispatchEvent(new CustomEvent('langchange', { detail: lang }));
  }

  var saved = null;
  try { saved = norm(localStorage.getItem(KEY)); } catch (e) {}
  if (saved) root.lang = saved;  // otherwise keep the page's own default

  document.addEventListener('DOMContentLoaded', function () {
    apply(norm(root.lang) || 'en', false);
    document.querySelectorAll('.lang-switch').forEach(function (b) {
      b.addEventListener('click', function () { apply(root.lang === 'ja' ? 'en' : 'ja', true); });
    });
  });
})();
