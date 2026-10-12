(() => {
  const timer = document.querySelector(".study-timer");
  const value = document.querySelector(".study-timer-value");
  if (!timer || !value) return;

  // Each page visit owns its timer; no account, storage, or shared state.
  let startedAt = Date.now();
  let interval;
  function render() {
    const elapsed = Math.max(0, Math.floor((Date.now() - startedAt) / 1000));
    const hours = Math.floor(elapsed / 3600);
    const minutes = Math.floor(elapsed / 60) % 60;
    const seconds = elapsed % 60;
    value.textContent = [hours, minutes, seconds]
      .map((part) => String(part).padStart(2, "0"))
      .join(":");
  }

  function start() {
    clearInterval(interval);
    startedAt = Date.now();
    render();
    interval = setInterval(render, 1000);
  }

  timer.hidden = false;
  start();
  // Returning from another tab keeps counting, including time reading PDFs.
  document.addEventListener("visibilitychange", render);
  window.addEventListener("pagehide", () => clearInterval(interval));
  // Browser Back can restore a cached page without executing its scripts again.
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) start();
  });
})();
