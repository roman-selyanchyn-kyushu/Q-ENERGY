(() => {
  const STORAGE_KEY = 'qenergy-lang';
  const videos = {
    2025: { id: 'srLEu440lV8', image: 'assets/video/summer-camp-2025.jpg', caption: 'Summer camp 2025 on YouTube' },
    2024: { id: '0SzLgqBV_yI', image: 'assets/video/summer-camp-2024.jpg', caption: 'Summer camp 2024 on YouTube' },
    2023: { id: 'qsMBEsDCcKI', image: 'assets/video/summer-camp-2023.jpg', caption: 'Summer camp 2023 on YouTube' },
    2022: { id: 'N8owTZyTvgg', image: 'assets/video/summer-camp-2022.jpg', caption: 'Summer camp 2022 on YouTube' }
  };
  const getInitialLang = () => localStorage.getItem(STORAGE_KEY) || (document.documentElement.lang === 'en' ? 'en' : 'ja');
  const applyLang = (lang) => {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-ja][data-en]').forEach((el) => {
      el.textContent = el.dataset[lang];
    });
    // Update pill toggle state (data-lang uses 'en'/'jp', html lang uses 'en'/'ja')
    const pillLang = lang === 'ja' ? 'jp' : 'en';
    const toggle = document.getElementById('lang-toggle');
    if (toggle) {
      toggle.setAttribute('data-lang', pillLang);
      toggle.querySelectorAll('button[data-set-lang]').forEach((b) => {
        const on = b.dataset.setLang === pillLang;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }
    localStorage.setItem(STORAGE_KEY, lang);
  };
  const setSummerVideo = (year) => {
    const data = videos[year] || videos[2025];
    const link = document.querySelector('[data-video-link]');
    const img = document.querySelector('[data-video-image]');
    const caption = document.querySelector('[data-video-caption]');
    if (!link || !img || !caption) return;
    link.href = `https://www.youtube.com/watch?v=${data.id}`;
    link.dataset.videoId = data.id;
    link.setAttribute('aria-label', `Watch Summer camp ${year} on YouTube`);
    img.src = data.image;
    img.alt = `Summer camp ${year} video thumbnail`;
    caption.textContent = data.caption;
    caption.dataset.ja = data.caption;
    caption.dataset.en = data.caption;
    document.querySelectorAll('[data-video-year]').forEach((button) => {
      const active = button.dataset.videoYear === String(year);
      button.classList.toggle('active', active);
      button.setAttribute('aria-selected', active ? 'true' : 'false');
    });
  };
  // Play the summer-camp videos in an on-page lightbox instead of sending people to
  // YouTube. The thumbnail stays a real <a href> so no-JS, cmd-click and middle-click
  // still open YouTube normally — only a plain left-click is intercepted.
  const modal = document.querySelector('[data-video-modal]');
  const modalSlot = modal && modal.querySelector('[data-video-modal-slot]');
  let lastFocused = null;
  const closeVideo = () => {
    if (!modal || !modal.classList.contains('open')) return;
    modal.classList.remove('open');
    modalSlot.replaceChildren(); // dropping the iframe is what stops playback
    document.body.classList.remove('modal-open');
    if (lastFocused) lastFocused.focus();
  };
  const openVideo = (id, label) => {
    if (!modal || !id) return;
    lastFocused = document.activeElement;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    iframe.title = label;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    modalSlot.replaceChildren(iframe);
    modal.setAttribute('aria-label', label);
    modal.classList.add('open');
    document.body.classList.add('modal-open');
    const closeBtn = modal.querySelector('[data-video-modal-close]');
    if (closeBtn) closeBtn.focus();
  };
  document.addEventListener('DOMContentLoaded', () => {
    applyLang(getInitialLang());
    setSummerVideo('2025');
    const videoLink = document.querySelector('[data-video-link]');
    if (videoLink && modal) {
      videoLink.addEventListener('click', (event) => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        openVideo(videoLink.dataset.videoId, videoLink.getAttribute('aria-label') || 'Summer camp video');
      });
      modal.addEventListener('click', (event) => {
        if (event.target === modal) closeVideo();
      });
      const closeBtn = modal.querySelector('[data-video-modal-close]');
      if (closeBtn) closeBtn.addEventListener('click', closeVideo);
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') closeVideo();
      });
    }
    document.querySelectorAll('#lang-toggle button[data-set-lang]').forEach((button) => {
      button.addEventListener('click', () => applyLang(button.dataset.setLang === 'jp' ? 'ja' : 'en'));
    });
    document.querySelectorAll('[data-video-year]').forEach((button) => {
      button.addEventListener('click', () => setSummerVideo(button.dataset.videoYear));
    });
  });
})();
