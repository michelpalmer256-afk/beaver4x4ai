(() => {
  const track = document.querySelector('.showcase-track');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if (track) {
    const slides = [...track.children];
    const prev = document.querySelector('.showcase-arrow.prev');
    const next = document.querySelector('.showcase-arrow.next');
    const update = () => {
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    };
    const move = direction => {
      const current = slides.reduce((best, el, i) =>
        Math.abs(el.offsetLeft - slides[0].offsetLeft - track.scrollLeft) <
        Math.abs(slides[best].offsetLeft - slides[0].offsetLeft - track.scrollLeft) ? i : best, 0);
      const target = slides[Math.max(0, Math.min(slides.length - 1, current + direction))];
      track.scrollTo({left: target.offsetLeft - slides[0].offsetLeft, behavior: reduced.matches ? 'instant' : 'smooth'});
    };
    prev.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    track.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        e.preventDefault(); move(e.key === 'ArrowRight' ? 1 : -1);
      }
    });
    track.addEventListener('scroll', update, {passive:true});
    new ResizeObserver(update).observe(track);
    update();
  }
  document.querySelectorAll('.menu-links a').forEach(a => a.addEventListener('click', () => {
    document.querySelector('.mobile-menu').open = false;
  }));
  if (!reduced.matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {entry.target.classList.add('scroll-visible');observer.unobserve(entry.target);}
    }), {threshold:.1});
    document.querySelectorAll('.feature,.showcase-intro,.photo').forEach(el => observer.observe(el));
  }
  document.addEventListener('visibilitychange', () => document.documentElement.classList.toggle('motion-paused', document.hidden));
})();

// Enhance only visible scenes; the landscapes remain readable without JavaScript.
(() => {
  const scenes = [...document.querySelectorAll('.explore-scene')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if (!scenes.length || !('IntersectionObserver' in window)) return;
  const visible = new Set();
  let frame = 0;
  const render = () => {
    frame = 0;
    visible.forEach(scene => {
      const box = scene.getBoundingClientRect();
      const shift = Math.max(-18, Math.min(18, (innerHeight / 2 - box.top - box.height / 2) * .045));
      scene.style.setProperty('--explore-shift', `${shift.toFixed(1)}px`);
    });
  };
  const schedule = () => { if (!reduced.matches && !frame) frame = requestAnimationFrame(render); };
  const observer = new IntersectionObserver(entries => {
    entries.forEach(({target, isIntersecting}) => {
      if (isIntersecting) {
        visible.add(target);
        target.classList.remove('explore-pending');
      } else visible.delete(target);
    });
    schedule();
  }, {threshold:0});
  scenes.forEach(scene => {
    if (!reduced.matches && scene.getBoundingClientRect().top >= innerHeight) scene.classList.add('explore-pending');
    observer.observe(scene);
  });
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  reduced.addEventListener('change', () => {
    scenes.forEach(scene => {
      scene.classList.remove('explore-pending');
      scene.style.removeProperty('--explore-shift');
    });
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    schedule();
  });
})();
