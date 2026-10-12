(() => {
  const string = document.querySelector(".rule-string");
  const path = string?.querySelector("path");
  if (!path) return;
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  let animation;
  let scrollFrame;
  let inView = false;

  function pluck() {
    cancelAnimationFrame(animation);
    const start = performance.now();
    function draw(now) {
      const t = (now - start) / 1000;
      if (t >= 1.4 || reducedMotion.matches) {
        path.setAttribute("d", "M0 0 L1000 0");
        return;
      }
      const amplitude = 8 * Math.exp(-3.2 * t) * Math.sin(2 * Math.PI * 5 * t);
      const points = [];
      for (let x = 0; x <= 1000; x += 20) {
        const y = amplitude * Math.sin(Math.PI * x / 1000);
        points.push(`${x === 0 ? "M" : "L"}${x} ${y.toFixed(3)}`);
      }
      path.setAttribute("d", points.join(" "));
      animation = requestAnimationFrame(draw);
    }
    animation = requestAnimationFrame(draw);
  }

  // Pluck only this divider when scrolling brings it into the reading area.
  window.addEventListener("scroll", () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      scrollFrame = undefined;
      const rect = string.getBoundingClientRect();
      const visible = rect.top < innerHeight * 0.85 && rect.bottom > innerHeight * 0.1;
      if (visible && !inView && !reducedMotion.matches) pluck();
      inView = visible;
    });
  }, { passive: true });
})();
