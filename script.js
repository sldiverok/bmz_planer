// scripts/script.js
async function loadCSV(departmentCode = null) {
  const response = await fetch('https://raw.githubusercontent.com/sldiverok/bmz_planer/refs/heads/main/bmz.csv');
  const data = await response.text();

  const rows = data.split('\n').map(r => r.trim()).filter(r => r);
  const headers = rows[0].split(',');

  const container = document.getElementById('table-container');
  let html = '<table><thead><tr>';
  headers.forEach(h => (html += `<th>${h}</th>`));
  html += '</tr></thead><tbody>';

  for (let i = 1; i < rows.length; i++) {
    const cols = rows[i].split(',');
    const row = {};
    headers.forEach((h, j) => (row[h] = cols[j]));

    if (!departmentCode || row['ПідрозділКод'] === departmentCode) {
      html += '<tr>';
      headers.forEach(h => (html += `<td>${row[h] || ''}</td>`));
      html += '</tr>';
    }
  }

  html += '</tbody></table>';
  container.innerHTML = html;
}
