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
    button.addEventListener("click", () => {
      theme = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = theme;
      button.setAttribute("aria-pressed", String(theme === "dark"));
      try {
        localStorage.setItem(storageKey, theme);
      } catch {
        // Keep the chosen theme for this page even without persistence.
      }
    });
  });
})();
