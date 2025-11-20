import csv, os, shutil

CSV_PATH = "bmz.csv"
PHOTOS_DIR = "photos"
PLACEHOLDER = "A_placeholder_digital_image_in_landscape_orientati.png"  # локальна заглушка

os.makedirs(PHOTOS_DIR, exist_ok=True)

created = 0
skipped = 0

with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        pib_lat = (row.get("ПІБ_лат") or row.get("\ufeffПІБ_лат") or "").strip()
        if not pib_lat:
            skipped += 1
            continue

        dest_path = os.path.join(PHOTOS_DIR, f"{pib_lat}.jpg")
        if not os.path.exists(dest_path):
            shutil.copyfile(PLACEHOLDER, dest_path)
            created += 1

print(f"✅ Створено {created} фото-заглушок у '{PHOTOS_DIR}/'")
if skipped:
    print(f"⚠️ Пропущено {skipped} записів без ПІБ_лат")
