import { NAV } from "./config.js";
import { renderNav } from "./nav.js";

renderNav();

const pages = NAV.map(item => item.file);
const current = location.pathname.split("/").pop() || "index.html";
const index = pages.indexOf(current);
const nav = document.getElementById("nav");
const toggle = document.getElementById("navToggle");

function setMenu(open) {
  if (!nav || !toggle) return;
  nav.classList.toggle("open", open);
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute(
    "aria-label",
    open ? "Navigation schließen" : "Navigation öffnen"
  );
}

toggle?.addEventListener("click", () => {
  setMenu(toggle.getAttribute("aria-expanded") !== "true");
});

const pager = document.getElementById("pager");
if (pager && index >= 0) {
  pager.className = "pager";
  pager.innerHTML = `
    ${index > 0 ? `<a href="${pages[index - 1]}">← Zurück</a>` : "<span></span>"}
    ${index < pages.length - 1
      ? `<a href="${pages[index + 1]}">Weiter →</a>`
      : '<a href="index.html">Startseite</a>'}
  `;
}

document.addEventListener("keydown", event => {
  if (event.altKey || event.ctrlKey || event.metaKey) return;
  if (event.target.matches("input, textarea, select, [contenteditable='true']")) return;

  if (event.key === "Escape") {
    setMenu(false);
    toggle?.focus();
    return;
  }

  if (event.key.toLowerCase() === "m") {
    setMenu(true);
    return;
  }

  if (event.key === "ArrowLeft" && index > 0) {
    location.href = pages[index - 1];
    return;
  }

  if (event.key === "ArrowRight" && index >= 0 && index < pages.length - 1) {
    location.href = pages[index + 1];
    return;
  }

  const shortcuts = {
    "1": pages[0],
    "2": pages[1],
    "3": pages[2],
    "4": pages[3],
    h: "index.html"
  };

  const destination = shortcuts[event.key.toLowerCase()];
  if (destination) location.href = destination;
});
