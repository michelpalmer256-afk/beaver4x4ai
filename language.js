// Static, reviewed translations. No network translation service and no dependencies.
(() => {
  'use strict';
  const root = new URL('./', document.currentScript.src);
  const current = new URL(location.href);
  const relative = current.pathname.slice(root.pathname.length);
  const pathLanguage = relative.startsWith('en/') ? 'en' : 'fr';
  const page = relative.replace(/^en\//, '').replace(/^index\.html$/, '');
  const explicit = current.searchParams.get('lang');
  let saved;
  try { saved = localStorage.getItem('beaver-language'); } catch (_) {}
  const valid = value => value === 'fr' || value === 'en';
  const browserLanguage = (navigator.languages?.[0] || navigator.language || '').toLowerCase().startsWith('fr') ? 'fr' : 'en';
  const language = valid(explicit) ? explicit : pathLanguage === 'en' ? 'en' : valid(saved) ? saved : browserLanguage;
  const address = lang => {
    const target = new URL((lang === 'en' ? 'en/' : '') + page, root);
    target.search = current.search;
    target.searchParams.delete('lang');
    if (lang === 'fr') target.searchParams.set('lang', 'fr');
    target.hash = location.hash;
    return target;
  };
  if (valid(explicit) || !valid(saved)) {
    try { localStorage.setItem('beaver-language', language); } catch (_) {}
  }
  if (language !== pathLanguage) {
    location.replace(address(language).href);
    return;
  }
  const prepare = () => {
    document.querySelectorAll('[data-language]').forEach(link => {
      const choice = link.dataset.language;
      link.href = address(choice).href;
      if (choice === language) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
      link.addEventListener('click', () => {
        link.href = address(choice).href;
        try { localStorage.setItem('beaver-language', choice); } catch (_) {}
      });
    });
    // Keep the current French context even when storage is unavailable.
    if (language === 'fr') document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || link.hasAttribute('data-language')) return;
      const target = new URL(link.href);
      if (target.origin === root.origin && target.pathname.startsWith(root.pathname) && (target.pathname.endsWith('.html') || target.pathname.endsWith('/'))) {
        target.searchParams.set('lang', 'fr');
        link.href = target.href;
      }
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', prepare, {once:true});
  else prepare();
  addEventListener('hashchange', () => document.querySelectorAll('[data-language]').forEach(link => { link.hash = location.hash; }));
})();
