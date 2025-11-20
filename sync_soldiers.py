import csv, os

CSV_PATH = "bmz.csv"
SOLDIERS_DIR = "soldiers"

# 1️⃣ Читаємо список актуальних ПІБ_лат з таблиці
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    valid_names = {row["ПІБ_лат"].strip() for row in reader if row.get("ПІБ_лат")}

# 2️⃣ Перевіряємо наявні файли в папці soldiers/
existing_files = {os.path.splitext(f)[0] for f in os.listdir(SOLDIERS_DIR) if f.endswith(".html")}

# 3️⃣ Знаходимо різниці
to_add = valid_names - existing_files
to_delete = existing_files - valid_names

print(f"🟩 Нових до створення: {len(to_add)}")
print(f"🟥 Зайвих до видалення: {len(to_delete)}")

# 4️⃣ Видаляємо зайві файли
for name in to_delete:
    path = os.path.join(SOLDIERS_DIR, f"{name}.html")
    os.remove(path)
    print(f"❌ Видалено: {path}")

# 5️⃣ Створюємо відсутні файли
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pib_lat = (row.get("ПІБ_лат") or row.get("\ufeffПІБ_лат") or "").strip()
        if pib_lat in to_add:
            html_path = os.path.join(SOLDIERS_DIR, f"{pib_lat}.html")
            with open(html_path, "w", encoding="utf-8") as out:
                out.write(f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>{row['ПІБ']}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>{row['ПІБ']}</h2>
<p><b>Підрозділ:</b> {row.get('Підрозділ','')}</p>
<p><b>Посада:</b> {row.get('Посада','')}</p>
<p><b>Військове звання:</b> {row.get('Військове звання','')}</p>
<p><b>ШПК:</b> {row.get('ШПК','')}</p>
<img src="../photos/{pib_lat}.jpg" alt="{row['ПІБ']}" width="200">
</body>
</html>""")
            print(f"✅ Створено: {html_path}")

print("\n✅ Синхронізацію завершено.")
