const halt = document.getElementById("halt");
const bewertung = document.getElementById("bewertung");
const bewertungOut = document.getElementById("bewertungOut");
const tiefe = document.getElementById("tiefe");
const status = document.getElementById("liveStatus");
const report = document.getElementById("report");

function validate() {
  const validTiefe =
    tiefe.value !== "" &&
    Number(tiefe.value) >= 0 &&
    Number(tiefe.value) <= 100;

  const ready =
    halt.checked &&
    Number(bewertung.value) >= 75 &&
    validTiefe;

  bewertungOut.value = bewertung.value;
  status.textContent = `STATUS ${ready ? "READY" : "WARN"}`;
  status.className = `card ${ready ? "ready" : "warn"}`;

  report.textContent =
    `HALT       ${halt.checked ? "✓" : "FEHLT"}\n` +
    `BEWERTUNG  ${bewertung.value}%\n` +
    `TIEFE      ${validTiefe ? tiefe.value : "UNGÜLTIG"}\n` +
    `STATUS     ${ready ? "READY" : "WARN"}`;
}

[halt, bewertung, tiefe].forEach(input =>
  input.addEventListener("input", validate)
);

validate();
