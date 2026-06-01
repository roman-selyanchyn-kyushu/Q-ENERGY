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
    document.querySelectorAll('[data-lang-toggle]').forEach((button) => {
      button.textContent = lang === 'ja' ? 'EN' : '日本語';
      button.setAttribute('aria-label', lang === 'ja' ? 'Switch language to English' : '日本語に切り替え');
    });
    localStorage.setItem(STORAGE_KEY, lang);
  };
  const setSummerVideo = (year) => {
    const data = videos[year] || videos[2025];
    const link = document.querySelector('[data-video-link]');
    const img = document.querySelector('[data-video-image]');
    const caption = document.querySelector('[data-video-caption]');
    if (!link || !img || !caption) return;
    link.href = `https://www.youtube.com/watch?v=${data.id}`;
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
  document.addEventListener('DOMContentLoaded', () => {
    applyLang(getInitialLang());
    setSummerVideo('2025');
    document.querySelectorAll('[data-lang-toggle]').forEach((button) => {
      button.addEventListener('click', () => applyLang(document.documentElement.lang === 'ja' ? 'en' : 'ja'));
    });
    document.querySelectorAll('[data-video-year]').forEach((button) => {
      button.addEventListener('click', () => setSummerVideo(button.dataset.videoYear));
    });
  });
})();
