import pandas as pd
import os
import re

CSV_FILE = "bmz.csv"
OUT_DIR = "soldiers"
INDEX_FILE = "index.html"

os.makedirs(OUT_DIR, exist_ok=True)

# === Функція для латинізації прізвища ===
def transliterate(name):
    table = {
        "А":"A","Б":"B","В":"V","Г":"H","Ґ":"G","Д":"D","Е":"E","Є":"Ye",
        "Ж":"Zh","З":"Z","И":"Y","І":"I","Ї":"Yi","Й":"Y","К":"K","Л":"L",
        "М":"M","Н":"N","О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U",
        "Ф":"F","Х":"Kh","Ц":"Ts","Ч":"Ch","Ш":"Sh","Щ":"Shch","Ю":"Yu",
        "Я":"Ya","Ь":"","’":"","'":""
    }
    result = "".join([table.get(ch.upper(), ch) if ch.isalpha() else ch for ch in name])
    return re.sub(r'[^a-zA-Z0-9]', '', result.lower())

# === Читаємо таблицю ===
df = pd.read_csv(CSV_FILE)

# === Генерація індивідуальних сторінок ===
for _, row in df.iterrows():
    pib = str(row.get("ПІБ", "")).strip()
    unit = str(row.get("Підрозділ", "—")).strip()
    posada = str(row.get("Посада", "—")).strip()
    code = str(row.get("ШПК", "—")).strip()

    if not pib or pib == "nan":
        continue

    filename = transliterate(pib.split()[0]) + ".html"
    path = os.path.join(OUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>{pib} — Дані військовослужбовця</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="card">
    <h2>{pib}</h2>
    <p><strong>Підрозділ:</strong> {unit}</p>
    <p><strong>Посада:</strong> {posada}</p>
    <p><strong>ШПК:</strong> {code}</p>
    <p><strong>Телефон:</strong> (вкажіть)</p>
    <p><strong>Адреса:</strong> (вкажіть)</p>
    <p><strong>Додаткова інформація:</strong> —</p>
    <a href="../index.html" class="back-btn">⬅ Повернутись</a>
  </div>
</body>
</html>""")

print(f"[ok] Створено {len(df)} файлів у {OUT_DIR}/")

# === Генеруємо index.html ===
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>Штатно-посадова книга БМЗ</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>📘 Штатно-посадова книга БМЗ</h1>
  <table>
  <tr><th>№</th><th>ПІБ</th><th>Підрозділ</th><th>Посада</th><th>ШПК</th></tr>
""")

    for i, row in df.iterrows():
        pib = str(row.get("ПІБ", "")).strip()
        unit = str(row.get("Підрозділ", "—")).strip()
        posada = str(row.get("Посада", "—")).strip()
        code = str(row.get("ШПК", "—")).strip()
        link = f"soldiers/{transliterate(pib.split()[0])}.html"

        f.write(f"<tr><td>{i+1}</td><td><a href='{link}'>{pib}</a></td><td>{unit}</td><td>{posada}</td><td>{code}</td></tr>\n")

    f.write("</table>\n</body>\n</html>")

print(f"[ok] Оновлено {INDEX_FILE}")
