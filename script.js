// === ДОВІДНИК БМЗ v2 ===
console.log("[build] script.js reloaded ✅");

async function loadCSV(departmentCode = null, admin = false) {
  try {
    console.log("[info] Завантаження CSV...");

    // --- Перевірка пароля ---
    if (admin) {
      const input = prompt("🔐 Введіть пароль для доступу:");
      const hash = md5(input || "");

      const ADMIN_HASH = "21232f297a57a5a743894a0e4a801fc3"; // admin
      const RZB_HASH = "71bc76c44acc7d6b977f60090dc866f7"; // rzb

      if (hash === ADMIN_HASH) {
        console.log("[ok] ADMIN доступ");
        departmentCode = null;
      } else if (hash === RZB_HASH) {
        console.log("[ok] RZB доступ");
        departmentCode = "RZB";
      } else {
        document.body.innerHTML =
          "<h2 style='color:red;text-align:center;margin-top:40px;'>❌ Доступ заборонено</h2>";
        return;
      }
    }

    // --- Завантаження CSV ---
    const response = await fetch(
      "https://raw.githubusercontent.com/sldiverok/bmz_planer/refs/heads/main/bmz.csv"
    );
    if (!response.ok) throw new Error("Не вдалося завантажити bmz.csv");

    const data = await response.text();
    const rows = data.split("\n").map((r) => r.trim()).filter((r) => r);
    const headers = rows[0].split(";");

    const container = document.getElementById("table-container");
    let html = "<table><thead><tr>";
    headers.forEach((h) => (html += `<th>${h}</th>`));
    html += "</tr></thead><tbody>";

    let matchCount = 0;

    for (let i = 1; i < rows.length; i++) {
      const cols = rows[i].split(";");
      const row = {};
      headers.forEach((h, j) => (row[h] = cols[j] || ""));
      if (!departmentCode || row["ПідрозділКод"] === departmentCode) {
        html += "<tr>";
        headers.forEach((h) => (html += `<td>${row[h]}</td>`));
        html += "</tr>";
        matchCount++;
      }
    }

    html += "</tbody></table>";
    container.innerHTML = html;

    console.log(`[ok] Таблиця побудована (${matchCount} рядків)`);
  } catch (err) {
    console.error("[ERR]", err);
    document.getElementById("table-container").innerHTML =
      "<p style='color:red;text-align:center;'>Помилка при завантаженні даних.</p>";
  }
}

function md5(str) {
  return CryptoJS.MD5(str).toString();
}
