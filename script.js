const menu=document.getElementById('menu'),nav=document.getElementById('navigation');if(menu&&nav){menu.addEventListener('click',()=>{const opened=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(opened));menu.textContent=opened?'✕':'☰'});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.textContent='☰'}))}

// Apparition progressive des sections, sans bloquer les navigateurs anciens.
const revealElements=document.querySelectorAll('.section-head,.feature,.split-copy,.trail-visual,.community,.copilot-inner,.download .wrap');
if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target)}})},{threshold:.08,rootMargin:'0px 0px -30px 0px'});revealElements.forEach(el=>{el.classList.add('reveal');observer.observe(el)})}
