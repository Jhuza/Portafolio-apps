/* Progressive enhancement: content stays visible if motion is unavailable. */
(() => {
  window.__jhgMotion?.destroy();
  const seen = window.__jhgMotionSeen ||= new WeakSet();
  const observed = new WeakSet();
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const animations = new Set();
  let frame = 0;
  let scanFrame = 0;
  let header = null;
  let slot = null;
  let naturalHeight = 0;
  let floating = false;
  let lastWidth = 0;
  const selector = '.aurora-hero-copy > *, .aurora-sculpture, .aurora-summary > span, .jhg-section > *, .aurora-project, .jhg-footer > *, .jhg-result-count, [data-testid="stExpander"], [data-testid="stSelectbox"], [data-testid="stTextInput"]';

  function reveal(element) {
    if (seen.has(element)) return;
    seen.add(element);
    if (preference.matches || !element.animate || element.contains(document.activeElement)) return;
    const siblings = element.parentElement?.children;
    const index = siblings ? Array.prototype.indexOf.call(siblings, element) : 0;
    const animation = element.animate(
      [{opacity: 0, translate: '0 14px'}, {opacity: 1, translate: '0 0'}],
      {duration: 540, delay: Math.min(index % 3 * 45, 90), easing: 'cubic-bezier(.22,1,.36,1)'}
    );
    animations.add(animation);
    animation.onfinish = animation.oncancel = () => animations.delete(animation);
  }
  const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      reveal(entry.target);
      observer.unobserve(entry.target);
    }
  }, {threshold: 0.06}) : null;

  function restoreHeader() {
    header?.classList.remove('jhg-is-floating');
    if (header) for (const key of ['left', 'width', 'top']) header.style.removeProperty(key);
    slot?.style.removeProperty('min-height');
    floating = false;
  }

  function updateHeader() {
    frame = 0;
    if (!header?.isConnected || !slot?.isConnected) return;
    const rect = slot.getBoundingClientRect();
    // Measure the regular layout on resize, including the two-row mobile header.
    if (Math.abs(rect.width - lastWidth) > 1) {
      restoreHeader();
      naturalHeight = header.getBoundingClientRect().height;
      lastWidth = rect.width;
    }
    if (!floating) naturalHeight = header.getBoundingClientRect().height;
    const toolbar = document.querySelector('[data-testid="stHeader"]');
    const top = Math.max(12, (toolbar?.getBoundingClientRect().bottom || 0) + 10);
    const shouldFloat = rect.top + naturalHeight < top + (floating ? 8 : 0);
    if (shouldFloat) {
      slot.style.minHeight = `${naturalHeight}px`;
      header.style.left = `${Math.max(12, rect.left)}px`;
      header.style.width = `${Math.min(rect.width, innerWidth - 24)}px`;
      header.style.top = `${top}px`;
      if (!floating) header.classList.add('jhg-is-floating');
      floating = true;
    } else if (floating) restoreHeader();
  }
  function scheduleHeader() {
    if (!frame) frame = requestAnimationFrame(updateHeader);
  }
  function scan() {
    scanFrame = 0;
    const next = document.querySelector('.jhg-header');
    if (next !== header) {
      restoreHeader();
      header = next;
      slot = header?.closest('.jhg-header-slot');
      lastWidth = 0;
    }
    if (!header) return;
    document.querySelector('[data-testid="stMainBlockContainer"]')?.querySelectorAll(selector).forEach(element => {
      if (seen.has(element) || observed.has(element)) return;
      observed.add(element);
      if (observer) observer.observe(element); else reveal(element);
    });
    scheduleHeader();
  }
  function scheduleScan() {
    if (!scanFrame) scanFrame = requestAnimationFrame(scan);
  }
  function reduceMotion() {
    if (preference.matches) for (const animation of [...animations]) animation.cancel();
  }
  // Streamlit scrolls its main container; capture also handles the document fallback.
  document.addEventListener('scroll', scheduleHeader, {capture: true, passive: true});
  window.addEventListener('resize', scheduleScan, {passive: true});
  preference.addEventListener('change', reduceMotion);
  const mutations = new MutationObserver(scheduleScan);
  mutations.observe(document.body, {childList: true, subtree: true});
  window.__jhgMotion = {destroy() {
    observer?.disconnect();
    mutations.disconnect();
    document.removeEventListener('scroll', scheduleHeader, true);
    window.removeEventListener('resize', scheduleScan);
    preference.removeEventListener('change', reduceMotion);
    cancelAnimationFrame(frame);
    cancelAnimationFrame(scanFrame);
    for (const animation of [...animations]) animation.cancel();
    restoreHeader();
  }};
  scan();
})();
