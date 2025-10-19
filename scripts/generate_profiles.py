import csv
import os

# === ШЛЯХИ ===
CSV_FILE = "bmz.csv"
OUT_DIR = "soldiers"

# === ФУНКЦІЯ ТРАНСЛІТЕРАЦІЇ (єдина для всієї системи) ===
def translit(name):
    table = {
        'А':'A','Б':'B','В':'V','Г':'H','Ґ':'G','Д':'D','Е':'E','Є':'Ye','Ж':'Zh','З':'Z',
        'И':'Y','І':'I','Ї':'Yi','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P',
        'Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Shch',
        'Ю':'Yu','Я':'Ya','Ь':'','’':'','\'':'',
        'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','ж':'zh','з':'z',
        'и':'y','і':'i','ї':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p',
        'р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch',
        'ю':'iu','я':'ia','ь':'',' ':'_','-':'_'
    }
    return ''.join(table.get(c, c) for c in name)

# === ШАБЛОН HTML ===
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name}</title>
  <link rel="icon" type="image/png" href="../favicon.png">
  <style>
    body {{
      background-color: #1c1c1c;
      color: #f5f5f5;
      font-family: "Segoe UI", sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
    }}
    .card {{
      background-color: #242424;
      border: 2px solid #00c0c4;
      border-radius: 12px;
      padding: 30px 40px;
      box-shadow: 0 0 12px #00c0c4;
      max-width: 480px;
    }}
    h2 {{
      color: #00c0c4;
      margin-top: 0;
    }}
    p {{
      margin: 6px 0;
    }}
    a {{
      display: inline-block;
      margin-top: 20px;
      padding: 10px 18px;
      background-color: #00c0c4;
      color: white;
      text-decoration: none;
      border-radius: 6px;
      font-weight: bold;
    }}
    a:hover {{
      background-color: #00969a;
    }}
  </style>
</head>
<body>

  <div class="card">
    <h2>{name}</h2>
    <p><strong>Підрозділ:</strong> {unit}</p>
    <p><strong>Посада:</strong> {position}</p>
    <p><strong>ШПК:</strong> {rank}</p>
    <p><strong>Військове звання:</strong> {title}</p>
    <p><strong>ВОС:</strong> {vos}</p>
    <p><strong>Т/р (max):</strong> {tr}</p>

    <a id="backBtn" href="#">← Повернутись</a>
  </div>

  <script>
    const unit = sessionStorage.getItem("bmz_unit") || "{unit_code}";
    document.getElementById("backBtn").href = "../index.html?unit=" + encodeURIComponent(unit);
  </script>

</body>
</html>
"""

# === ЗАВАНТАЖЕННЯ CSV ===
def load_soldiers(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)

# === СТВОРЕННЯ СТОРІНОК ===
def generate_html_pages(soldiers):
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    for s in soldiers:
        name = s.get("ПІБ", "").strip()
        if not name:
            continue

        latin_name = translit(name.lower())
        s["ПІБ_лат"] = latin_name  # створюємо латинський варіант у даних

        filename = latin_name + ".html"
        filepath = os.path.join(OUT_DIR, filename)

        html = HTML_TEMPLATE.format(
            name=name,
            unit=s.get("Підрозділ", ""),
            position=s.get("Посада", ""),
            rank=s.get("ШПК", ""),
            title=s.get("Військове звання", ""),
            vos=s.get("ВОС", ""),
            tr=s.get("Т/р (max)", ""),
            unit_code=s.get("ПідрозділКод", "")
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[ok] {filename} створено")

# === ЗАПУСК ===
if __name__ == "__main__":
    soldiers = load_soldiers(CSV_FILE)
    generate_html_pages(soldiers)
    print(f"\n✅ Згенеровано {len(soldiers)} файлів у '{OUT_DIR}/'")
