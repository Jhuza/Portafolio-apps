/* One unlock per page load. Window state survives Streamlit filter reruns. */
(() => {
  window.__jhgVideo?.destroy();
  const state = window.__jhgVideoState ||= {started: false, completed: false, time: 0, manualPause: false};
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const main = document.querySelector('[data-testid="stMain"]');
  const scrollTop = () => main?.scrollTop || document.scrollingElement?.scrollTop || 0;
  let previousScroll = scrollTop();
  let video, root, button, finalImage, visibility, scanFrame = 0;
  let removers = [];
  let visible = false;
  const listen = (el, event, handler) => {
    el.addEventListener(event, handler);
    removers.push(() => el.removeEventListener(event, handler));
  };
  function label() {
    if (!button) return;
    button.hidden = state.completed;
    button.textContent = video.paused ? (state.started ? 'Continuar animación' : 'Ver animación') : 'Pausar animación';
    button.setAttribute('aria-label', button.textContent);
  }
  function complete() {
    state.completed = true;
    state.time = video.duration || state.time;
    video.pause();
    finalImage.hidden = false;
    root.dataset.heroState = 'complete';
    label();
  }
  async function play() {
    if (!video || state.completed) return;
    finalImage.hidden = true;
    try {
      await video.play();
      state.started = true;
      root.dataset.heroState = 'playing';
    } catch (_) {
      // Browser policy or a loading interruption: keep the explicit play button.
      root.dataset.heroState = 'ready';
    }
    label();
  }
  function release() {
    if (video && !state.completed) state.time = video.currentTime || state.time;
    removers.forEach(remove => remove());
    removers = [];
    visibility?.disconnect();
    button?.remove();
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
    video.controls = false;
    video.muted = true;
    video.loop = false;
    video.playsInline = true;
    video.preload = 'auto';
    video.poster = 'app/static/hero/closed.jpg';
    video.setAttribute('aria-label', 'Carpeta de cristal que revela las cinco modalidades del portafolio JHG');
    video.setAttribute('tabindex', '-1');
    finalImage = document.createElement('img');
    finalImage.className = 'jhg-video-final';
    finalImage.src = 'app/static/hero/open.jpg';
    finalImage.alt = 'JHG Portfolio Media: imagen a voz, hábitat inteligente, objetos IA, tablero propio y control por voz.';
    finalImage.hidden = !state.completed && !reduced.matches;
    root.append(finalImage);
    button = document.createElement('button');
    button.className = 'jhg-video-control';
    button.type = 'button';
    root.append(button);
    root.dataset.heroState = state.completed ? 'complete' : 'ready';
    listen(button, 'click', () => {
      if (video.paused) {
        state.manualPause = false;
        finalImage.hidden = true;
        play();
      } else {
        state.manualPause = true;
        video.pause();
      }
    });
    listen(video, 'timeupdate', () => { if (!state.completed) state.time = video.currentTime; });
    listen(video, 'ended', complete);
    listen(video, 'pause', label);
    listen(video, 'play', label);
    listen(video, 'error', () => {
      finalImage.hidden = false;
      button.hidden = true;
      root.dataset.heroState = 'unavailable';
    });
    const restore = () => {
      if (state.completed) { complete(); return; }
      if (state.time > 0 && Number.isFinite(video.duration)) video.currentTime = Math.min(state.time, video.duration);
    };
    if (video.readyState >= 1) restore(); else listen(video, 'loadedmetadata', restore);
    visibility = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting && entries[0].intersectionRatio >= 0.15;
      if (!visible) video.pause();
      else if (state.started && !state.manualPause && !state.completed && !reduced.matches && !document.hidden) play();
    }, {threshold: [0, 0.15]});
    visibility.observe(video);
    label();
  }
  function onScroll() {
    const current = scrollTop();
    const down = current > previousScroll + 1;
    previousScroll = current;
    if (down && visible && !reduced.matches && !state.started && !state.completed && !state.manualPause) play();
  }
  function onVisibility() {
    if (document.hidden) video?.pause();
    else if (visible && state.started && !state.completed && !state.manualPause && !reduced.matches) play();
  }
  function onPreference() {
    if (reduced.matches && video) {
      video.pause();
      finalImage.hidden = false;
    } else if (finalImage && !state.completed) finalImage.hidden = true;
  }
  const mutations = new MutationObserver(() => {
    if (!scanFrame) scanFrame = requestAnimationFrame(bind);
  });
  mutations.observe(document.body, {childList: true, subtree: true});
  document.addEventListener('scroll', onScroll, {capture: true, passive: true});
  document.addEventListener('visibilitychange', onVisibility);
  reduced.addEventListener('change', onPreference);
  window.__jhgVideo = {destroy() {
    release();
    mutations.disconnect();
    cancelAnimationFrame(scanFrame);
    document.removeEventListener('scroll', onScroll, true);
    document.removeEventListener('visibilitychange', onVisibility);
    reduced.removeEventListener('change', onPreference);
  }};
  bind();
})();
