// === ДОВІДНИК БМЗ з авторизацією ===
// Скрипт для завантаження bmz.csv і контролю доступу до admin.html
// Автор: sldiverok squad

async function loadCSV(departmentCode = null, admin = false) {
  try {
    console.log("[info] Завантаження даних з CSV...");

    // --- Перевірка пароля для admin ---
    if (admin) {
      const input = prompt("🔐 Введіть пароль для доступу до повного списку:");
      const hash = md5(input || "");
      const allowed = "21232f297a57a5a743894a0e4a801fc3"; // md5('admin')

      if (hash !== allowed) {
        document.body.innerHTML =
          "<h2 style='color:red;text-align:center;margin-top:40px;'>❌ Доступ заборонено</h2>";
        return;
      }
      console.log("[ok] Авторизація ADMIN успішна");
    }

    const response = await fetch(
      "https://raw.githubusercontent.com/sldiverok/bmz_planer/refs/heads/main/bmz.csv"
    );
    if (!response.ok) throw new Error("Не вдалося завантажити bmz.csv");

    const data = await response.text();
    const rows = data
      .split("\n")
      .map((r) => r.trim())
      .filter((r) => r.length > 0);
    const headers = rows[0].split(";");

    const container = document.getElementById("table-container");
    let html = "<table><thead><tr>";
    headers.forEach((h) => (html += `<th>${h}</th>`));
    html += "</tr></thead><tbody>";

    let matchCount = 0;

    for (let i = 1; i < rows.length; i++) {
      const cols = rows[i].split(";");
      const row = {};
      headers.forEach((h, j) => (row[h] = cols[j] ? cols[j].trim() : ""));

      if (!departmentCode || row["ПідрозділКод"] === departmentCode) {
        html += "<tr>";
        headers.forEach((h) => (html += `<td>${row[h] || ""}</td>`));
        html += "</tr>";
        matchCount++;
      }
    }

    html += "</tbody></table>";
    container.innerHTML = html;

    console.log(
      `[ok] Таблиця побудована. Рядків: ${matchCount}${
        departmentCode ? " (" + departmentCode + ")" : " (всі)"
      }`
    );

    if (matchCount === 0) {
      container.innerHTML +=
        "<p style='text-align:center;color:#aaa;margin-top:20px;'>Немає даних для цього підрозділу.</p>";
    }
  } catch (err) {
    console.error("[ERR] Помилка при завантаженні CSV:", err);
    const container = document.getElementById("table-container");
    container.innerHTML =
      "<p style='color:red;text-align:center;'>Помилка при завантаженні даних.</p>";
  }
}

// === Простий MD5 реалізатор для браузера ===
function md5(str) {
  return CryptoJS.MD5(str).toString();
}
