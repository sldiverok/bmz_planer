// === ДОВІДНИК БМЗ ===
// Скрипт для завантаження bmz.csv з GitHub і відображення таблиці з фільтром по ПідрозділКод
// Автор: sldiverok squad

async function loadCSV(departmentCode = null) {
  try {
    console.log("[info] Завантаження даних з CSV...");

    // Підтягуємо CSV безпосередньо з GitHub
    const response = await fetch(
      "https://raw.githubusercontent.com/sldiverok/bmz_planer/refs/heads/main/bmz.csv"
    );

    if (!response.ok) {
      throw new Error("Не вдалося завантажити bmz.csv");
    }

    const data = await response.text();

    // Розбиваємо файл на рядки
    const rows = data
      .split("\n")
      .map((r) => r.trim())
      .filter((r) => r.length > 0);

    if (rows.length === 0) {
      throw new Error("CSV файл порожній або має неправильний формат.");
    }

    // У CSV використовується роздільник ';'
    const headers = rows[0].split(";");

    console.log("[ok] Заголовки CSV:", headers);

    // Готуємо HTML для таблиці
    const container = document.getElementById("table-container");
    let html = "<table><thead><tr>";

    headers.forEach((h) => (html += `<th>${h}</th>`));
    html += "</tr></thead><tbody>";

    let matchCount = 0;

    for (let i = 1; i < rows.length; i++) {
      const cols = rows[i].split(";");
      const row = {};

      headers.forEach((h, j) => (row[h] = cols[j] ? cols[j].trim() : ""));

      // Якщо підрозділ не вказаний — показуємо все, якщо вказаний — тільки вибраний код
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
      `[ok] Таблиця побудована. Знайдено рядків: ${matchCount}${
        departmentCode ? " для " + departmentCode : ""
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

// === Кінець скрипту ===
