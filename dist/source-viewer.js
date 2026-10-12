(() => {
  document.querySelectorAll(".source-toggle").forEach((button) => {
    const row = button.closest("li");
    const course = row.querySelector("h3").textContent;
    const slug = button.dataset.source;
    const panel = document.createElement("section");
    panel.id = `source-${slug}`;
    panel.className = "source-panel";
    panel.hidden = true;
    panel.setAttribute("aria-label", `${course} LaTeX source`);

    const toolbar = document.createElement("div");
    toolbar.className = "source-toolbar";
    const copy = document.createElement("button");
    copy.type = "button";
    copy.textContent = "Copy";
    copy.disabled = true;
    toolbar.append(copy);
    const link = document.createElement("a");
    link.href = `./sources/${slug}.tex`;
    link.download = `${slug}.tex`;
    link.textContent = "Download .tex";
    toolbar.append(link);
    const status = document.createElement("p");
    status.className = "source-status";
    status.setAttribute("role", "status");
    const pre = document.createElement("pre");
    pre.tabIndex = 0;
    pre.setAttribute("aria-label", `${course} source code`);
    const code = document.createElement("code");
    pre.append(code);
    panel.append(toolbar, status, pre);
    row.append(panel);
    button.hidden = false;
    button.setAttribute("aria-controls", panel.id);

    let source;
    let loading = false;
    button.addEventListener("click", async () => {
      panel.hidden = !panel.hidden;
      button.setAttribute("aria-expanded", String(!panel.hidden));
      if (panel.hidden || source !== undefined || loading) return;
      loading = true;
      status.textContent = "Loading source…";
      try {
        const response = await fetch(`./sources/${slug}.tex`);
        if (!response.ok) throw new Error("Source unavailable");
        source = await response.text();
        code.textContent = source;
        copy.disabled = false;
        status.textContent = "";
      } catch {
        status.textContent = "Couldn't load the preview. Close and reopen to retry, or use the download link.";
      } finally {
        loading = false;
      }
    });

    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(source);
        status.textContent = "Source copied to clipboard.";
      } catch {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        pre.focus();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = "Source selected. Press Ctrl+C (or ⌘C) to copy.";
      }
    });
  });
})();
