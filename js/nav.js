import { NAV } from "./config.js";

export function renderNav() {
  const nav = document.getElementById("nav");
  if (!nav) return;

  const current = location.pathname.split("/").pop() || "index.html";

  nav.innerHTML = NAV.map(item => {
    const active = current === item.file;
    return `<a href="${item.file}"${active
      ? ' class="active" aria-current="page"'
      : ""}>${item.title}</a>`;
  }).join("");
}
