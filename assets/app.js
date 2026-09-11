(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  const header = document.querySelector('.site-header');
  let scrollTicking = false;
  function updateHeader() {
    scrollTicking = false;
    header?.classList.toggle('is-scrolled', window.scrollY > 0);
  }
  window.addEventListener('scroll', () => {
    if (!scrollTicking) {
      scrollTicking = true;
      requestAnimationFrame(updateHeader);
    }
  }, { passive: true });
  function closeMenu(returnFocus = false) {
    nav?.classList.remove('is-open');
    menu?.setAttribute('aria-expanded', 'false');
    if (menu) menu.textContent = 'Menú';
    if (returnFocus) menu?.focus();
  }
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    menu.textContent = open ? 'Cerrar' : 'Menú';
  });
  nav?.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  matchMedia('(min-width: 761px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
  });

  const search = document.querySelector('#news-search');
  const clearQuery = document.querySelector('#clear-query');
  const cards = [...document.querySelectorAll('[data-news-card]')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  let category = 'all';
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  function filterNews() {
    const query = normalize(search.value);
    if (clearQuery) clearQuery.hidden = search.value.length === 0;
    let total = 0;
    cards.forEach(card => {
      const categories = card.dataset.categories.split(' ');
      const matchesCategory = category === 'all' || categories.includes(category);
      const matchesQuery = normalize(card.textContent + ' ' + card.dataset.keywords).includes(query);
      card.hidden = !(matchesCategory && matchesQuery);
      if (!card.hidden) total++;
    });
    document.querySelector('#news-count').textContent = `${total} ${total === 1 ? 'noticia' : 'noticias'}`;
    document.querySelector('#no-results').hidden = total !== 0;
  }
  function selectFilter(value) {
    category = value;
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === value)));
    filterNews();
  }
  if (search) {
    clearQuery?.addEventListener('click', () => {
      search.value = '';
      filterNews();
      search.focus();
    });
    search.addEventListener('input', filterNews);
    filters.forEach(button => button.addEventListener('click', () => selectFilter(button.dataset.filter)));
    document.querySelector('#clear-search').addEventListener('click', () => {
      search.value = '';
      selectFilter('all');
      search.focus();
    });
    document.querySelector('.header-search').addEventListener('click', () => {
      closeMenu();
      setTimeout(() => search.focus({preventScroll:true}), 0);
    });
  }
  const preview = document.querySelector('.hero-preview');
  const motionAllowed = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 761px) and (prefers-reduced-motion: no-preference)');
  if (preview) {
    let frame = 0;
    const resetTilt = () => {
      cancelAnimationFrame(frame);
      preview.style.setProperty('--tilt-x', '0deg');
      preview.style.setProperty('--tilt-y', '0deg');
    };
    preview.addEventListener('pointermove', event => {
      if (!motionAllowed.matches || event.pointerType === 'touch') return;
      const rect = preview.getBoundingClientRect();
      const clamp = value => Math.max(-4, Math.min(4, value));
      const x = clamp(((event.clientY - rect.top) / rect.height - .5) * -8);
      const y = clamp(((event.clientX - rect.left) / rect.width - .5) * 8);
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        preview.style.setProperty('--tilt-x', `${x.toFixed(2)}deg`);
        preview.style.setProperty('--tilt-y', `${y.toFixed(2)}deg`);
      });
    });
    preview.addEventListener('pointerleave', resetTilt);
    preview.addEventListener('pointercancel', resetTilt);
    motionAllowed.addEventListener('change', resetTilt);
  }
  const sections = [...document.querySelectorAll('main section[id]')];
  if (sections.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const matched = nav.querySelector(`a[href="#${entry.target.id}"]`);
        if (!matched) return;
        nav.querySelectorAll('a').forEach(link => {
          link.classList.toggle('active', link === matched);
          if (link === matched) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, {rootMargin:'-15% 0px -60% 0px'});
    sections.forEach(section => observer.observe(section));
  }
})();
