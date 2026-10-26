/* Scroll-driven, progressively enhanced hero; no wheel/touch interception. */
(() => {
  window.__jhgVideo?.destroy();
  const state = window.__jhgScrollHero ||= {completed: false};
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let video, root, track, finalImage, rail, progress, hint, skip;
  let frame = 0, scanFrame = 0, targetTime = 0, travel = 1, pinTop = 150;
  let removers = [], resizeObserver, failed = false;
  const listen = (el, event, fn) => {
    el.addEventListener(event, fn);
    removers.push(() => el.removeEventListener(event, fn));
  };
  function finish() {
    state.completed = true;
    video.pause();
    finalImage.hidden = false;
    root.dataset.heroState = 'complete';
    hint.textContent = 'Tu colección está lista';
    skip.textContent = 'Explorar apps ↓';
    progress.style.setProperty('--progress', '1');
    progress.setAttribute('aria-valuenow', '100');
  }
  function seek() {
    if (!video || video.seeking || video.readyState < 1 || state.completed) return;
    if (Math.abs(video.currentTime - targetTime) > 1 / 48) video.currentTime = targetTime;
  }
  function update() {
    frame = 0;
    if (!video?.isConnected || !track?.isConnected || reduced.matches) return;
    const fraction = Math.max(0, Math.min(1, (pinTop - track.getBoundingClientRect().top) / travel));
    if (state.completed) return;
    progress.style.setProperty('--progress', String(fraction));
    progress.setAttribute('aria-valuenow', String(Math.round(fraction * 100)));
    if (!Number.isFinite(video.duration)) return;
    if (fraction >= 1) { finish(); return; }
    targetTime = fraction * Math.max(0, video.duration - 1 / 24);
    root.dataset.heroState = fraction > 0 ? 'scrubbing' : 'ready';
    seek();
  }
  function schedule() {
    if (!state.completed && !reduced.matches && !frame) frame = requestAnimationFrame(update);
  }
  function measure() {
    if (!root?.isConnected) return;
    const toolbar = document.querySelector('[data-testid="stHeader"]');
    const toolbarBottom = toolbar?.getBoundingClientRect().bottom || 60;
    pinTop = toolbarBottom + (innerWidth <= 640 ? 120 : 90);
    const mediaHeight = Math.max(140, innerHeight - pinTop - 90);
    travel = Math.max(700, innerHeight * 1.8);
    track.style.setProperty('--hero-top', `${pinTop}px`);
    track.style.setProperty('--hero-media-height', `${mediaHeight}px`);
    track.dataset.scrollHero = reduced.matches || failed ? 'reduced' : 'active';
    track.style.setProperty('--hero-track-height', `${track.firstElementChild.getBoundingClientRect().height + travel + 120}px`);
    schedule();
  }
  function release() {
    removers.forEach(remove => remove());
    removers = [];
    resizeObserver?.disconnect();
    rail?.remove();
    finalImage?.remove();
  }
  function bind() {
    scanFrame = 0;
    const next = document.querySelector('.st-key-jhg_video_hero video');
    if (next === video) return;
    release();
    video = next;
    if (!video) return;
    root = video.closest('.st-key-jhg_video_hero');
    track = root.closest('.st-key-jhg_hero_track');
    if (!track) return;
    video.pause();
    video.controls = false;
    video.muted = true;
    video.loop = false;
    video.playsInline = true;
    video.preload = reduced.matches ? 'none' : 'auto';
    video.poster = 'app/static/hero/closed.webp';
    video.setAttribute('aria-label', 'Carpeta JHG: animación de apertura controlada al desplazarte por la página');
    video.setAttribute('tabindex', '-1');
    finalImage = document.createElement('img');
    finalImage.className = 'jhg-video-final';
    finalImage.src = 'app/static/hero/open.webp';
    finalImage.alt = 'JHG Portfolio Media: imagen a voz, hábitat inteligente, objetos IA, tablero propio y control por voz.';
    finalImage.hidden = !state.completed && !reduced.matches;
    video.parentElement.append(finalImage);
    rail = document.createElement('div');
    rail.className = 'jhg-hero-rail';
    hint = document.createElement('span');
    hint.textContent = 'Desliza hacia abajo para abrir la colección';
    progress = document.createElement('div');
    progress.className = 'jhg-hero-progress';
    progress.setAttribute('role', 'progressbar');
    progress.setAttribute('aria-label', 'Apertura de la colección');
    progress.setAttribute('aria-valuemin', '0');
    progress.setAttribute('aria-valuemax', '100');
    progress.setAttribute('aria-valuenow', '0');
    skip = document.createElement('button');
    skip.className = 'jhg-video-control';
    skip.type = 'button';
    skip.textContent = 'Saltar animación ↓';
    rail.append(hint, progress, skip);
    root.append(rail);
    listen(skip, 'click', () => {
      finish();
      document.querySelector('#experiencias')?.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block: 'start'});
    });
    listen(video, 'loadedmetadata', schedule);
    listen(video, 'loadeddata', schedule);
    listen(video, 'seeked', seek);
    listen(video, 'error', () => {
      failed = true;
      finish();
      measure();
    });
    if (state.completed || reduced.matches) finish();
    measure();
    let lastWidth = track.clientWidth;
    resizeObserver = new ResizeObserver(() => {
      if (track.clientWidth !== lastWidth) { lastWidth = track.clientWidth; measure(); }
    });
    resizeObserver.observe(track);
  }
  function onPreference() {
    if (reduced.matches && video) finish();
    measure();
  }
  // Filter reruns may replace the video. Ignore unrelated text/card mutations.
  const mutations = new MutationObserver(() => {
    if (video?.isConnected || scanFrame) return;
    scanFrame = requestAnimationFrame(bind);
  });
  mutations.observe(document.body, {childList: true, subtree: true});
  document.addEventListener('scroll', schedule, {capture: true, passive: true});
  window.addEventListener('resize', measure, {passive: true});
  reduced.addEventListener('change', onPreference);
  window.__jhgVideo = {destroy() {
    release();
    mutations.disconnect();
    cancelAnimationFrame(frame);
    cancelAnimationFrame(scanFrame);
    document.removeEventListener('scroll', schedule, true);
    window.removeEventListener('resize', measure);
    reduced.removeEventListener('change', onPreference);
  }};
  bind();
})();
