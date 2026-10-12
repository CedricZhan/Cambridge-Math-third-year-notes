(() => {
  const root = document.documentElement;
  const storageKey = "cambridge-notes-theme";
  let theme = "light";
  try {
    if (localStorage.getItem(storageKey) === "dark") theme = "dark";
  } catch {
    // The switch still works when browser storage is unavailable.
  }
  root.dataset.theme = theme;

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".theme-toggle");
    if (!button) return;
    button.hidden = false;
    button.setAttribute("aria-pressed", String(theme === "dark"));
    let switching = false;
    function applyTheme(nextTheme) {
      theme = nextTheme;
      root.dataset.theme = theme;
      button.setAttribute("aria-pressed", String(theme === "dark"));
      try {
        localStorage.setItem(storageKey, theme);
      } catch {
        // Keep the chosen theme for this page even without persistence.
      }
    }

    button.addEventListener("click", async () => {
      if (switching) return;
      const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
      if (!document.startViewTransition || matchMedia("(prefers-reduced-motion: reduce)").matches) {
        applyTheme(nextTheme);
        return;
      }
      const rect = button.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;
      const radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      switching = true;
      let applied = false;
      try {
        const transition = document.startViewTransition(() => {
          applyTheme(nextTheme);
          applied = true;
        });
        // A hidden tab can cause the browser to skip the visual transition.
        transition.finished.catch(() => {});
        await transition.ready;
        await root.animate(
          { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`] },
          { duration: 650, easing: "cubic-bezier(0.22, 1, 0.36, 1)", pseudoElement: "::view-transition-new(root)" }
        ).finished;
        await transition.finished;
      } catch {
        if (!applied) applyTheme(nextTheme);
      } finally {
        switching = false;
      }
    });
  });
})();
