import pandas as pd
import os
import re

CSV_FILE = "bmz.csv"
OUT_DIR = "soldiers"
INDEX_FILE = "index.html"
LOG_FILE = "bad_lines.log"

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

# === Безпечне читання CSV ===
bad_lines = []
try:
    df = pd.read_csv(
        CSV_FILE,
        sep=';',
        encoding='utf-8',
        engine='python',
        on_bad_lines='skip'
    )
except Exception as e:
    print(f"[err] Не вдалося прочитати {CSV_FILE}: {e}")
    exit()

# === Перевірка наявності потрібної колонки ===
if "Прізвище, ім’я та по батькові" not in df.columns:
    print("[err] У файлі bmz.csv немає колонки 'Прізвище, ім’я та по батькові'. Перевір заголовки.")
    print(f"[debug] Знайдені колонки: {list(df.columns)}")
    exit()

# === Фільтруємо порожні записи ===
df = df.dropna(subset=["Прізвище, ім’я та по батькові"])
df = df[df["Прізвище, ім’я та по батькові"].astype(str).str.strip() != ""]

print(f"[info] Завантажено {len(df)} записів із {CSV_FILE}")

# === Генеруємо сторінки для кожного військовослужбовця ===
for _, row in df.iterrows():
    pib = str(row.get("Прізвище, ім’я та по батькові", "")).strip()
    unit = str(row.get("Підрозділ", "—")).strip()
    posada = str(row.get("Посада", "—")).strip()
    code = str(row.get("ШПК", "—")).strip()

    if not pib or pib.lower() == "nan":
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
  <style>
    body {{font-family: Arial, sans-serif; background-color:#1e1e1e; color:#eaeaea;}}
    .card {{background:#2b2b2b; margin:50px auto; padding:20px; width:420px; border-radius:12px; box-shadow:0 0 10px #00c0c4;}}
    a {{color:#00c0c4; text-decoration:none;}}
    .back-btn {{display:inline-block; margin-top:20px; border:1px solid #00c0c4; padding:5px 10px; border-radius:6px;}}
    .back-btn:hover {{background:#00c0c4; color:#1e1e1e;}}
  </style>
</head>
<body>
  <div class="card">
    <h2>{pib}</h2>
    <p><strong>Підрозділ:</strong> {unit}</p>
    <p><strong>Посада:</strong> {posada}</p>
    <p><strong>ШПК:</strong> {code}</p>
    <p><strong>Телефон:</strong> —</p>
    <p><strong>Адреса:</strong> —</p>
    <p><strong>Додаткова інформація:</strong> —</p>
    <a href="../index.html" class="back-btn">⬅ Повернутись</a>
  </div>
</body>
</html>""")

print(f"[ok] Створено {len(df)} файлів у '{OUT_DIR}/'")

# === Формуємо index.html ===
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>Штатно-посадова книга БМЗ</title>
  <link rel="stylesheet" href="style.css">
  <style>
    body {font-family: Arial, sans-serif; background-color:#1e1e1e; color:#eaeaea;}
    table {width:95%; margin:20px auto; border-collapse:collapse;}
    th,td {border:1px solid #333; padding:6px 10px;}
    th {background:#333; color:#00c0c4;}
    tr:nth-child(even){background:#2a2a2a;}
    tr:hover{background:#3a3a3a;}
    a{color:#00c0c4;text-decoration:none;}
  </style>
</head>
<body>
  <h1 style="text-align:center;">📘 Штатно-посадова книга БМЗ</h1>
  <table>
    <tr><th>№</th><th>ПІБ</th><th>Підрозділ</th><th>Посада</th><th>ШПК</th></tr>
""")

    for i, row in df.iterrows():
        pib = str(row.get("Прізвище, ім’я та по батькові", "")).strip()
        unit = str(row.get("Підрозділ", "—")).strip()
        posada = str(row.get("Посада", "—")).strip()
        code = str(row.get("ШПК", "—")).strip()
        link = f"soldiers/{transliterate(pib.split()[0])}.html"
        f.write(f"<tr><td>{i+1}</td><td><a href='{link}'>{pib}</a></td><td>{unit}</td><td>{posada}</td><td>{code}</td></tr>\n")

    f.write("</table>\n</body>\n</html>")

print(f"[ok] Оновлено '{INDEX_FILE}'")
