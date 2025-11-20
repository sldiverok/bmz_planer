import csv, os

CSV_PATH = "bmz.csv"
SOLDIERS_DIR = "soldiers"

# створюємо папку якщо немає
os.makedirs(SOLDIERS_DIR, exist_ok=True)

created = 0
skipped = []

with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        pib_lat = (row.get("ПІБ_лат") or row.get("\ufeffПІБ_лат") or "").strip()
        pib = (row.get("ПІБ") or "").strip()
        rank = (row.get("Військове звання") or "").strip()
        unit = (row.get("Підрозділ") or "").strip()
        posada = (row.get("Посада") or "").strip()
        shpk = (row.get("ШПК") or "").strip()

        # перевіряємо наявність обов'язкових полів
        if not (pib_lat and pib and rank):
            skipped.append(pib or "[без ПІБ]")
            continue

        html_path = os.path.join(SOLDIERS_DIR, f"{pib_lat}.html")
        with open(html_path, "w", encoding="utf-8") as out:
            out.write(f'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>{pib}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>{rank} {pib}</h2>
<p><b>Підрозділ:</b> {unit}</p>
<p><b>Посада:</b> {posada}</p>
<p><b>ШПК:</b> {shpk}</p>
<img src="../BIO/{pib_lat}.jpg" alt="{pib}" width="220">
</body>
</html>''')
        created += 1

print(f"✅ Згенеровано {created} сторінок у '{SOLDIERS_DIR}/'")
if skipped:
    print(f"⚠️ Пропущено {len(skipped)} записів без повних даних (приклади): {skipped[:10]}")
