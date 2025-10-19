#!/usr/bin/env python3
# check_missing_pages.py
# UTF-8

import csv
import os
import sys
from difflib import get_close_matches

CSV_FILE = "bmz.csv"
HTML_DIR = "soldiers"
OUT_SIMPLE = "missing_pages.txt"
OUT_SUGGEST = "missing_with_suggestions.txt"
CLOSE_MATCH_N = 5
CLOSE_MATCH_CUTOFF = 0.6  # від 0.0 до 1.0 — регулюй чутливість

def detect_delimiter(path):
    with open(path, "rb") as fh:
        start = fh.read(2048)
    try:
        s = start.decode("utf-8-sig")
    except Exception:
        s = start.decode("cp1251", errors="ignore")
    # перевіряємо основні роздільники
    if ";" in s and s.count(";") > s.count(","):
        return ";"
    if "," in s:
        return ","
    return ","  # запасний варіант

def find_lat_column(headers):
    # нормалізуємо заголовки для пошуку
    norm = [(h, h.strip().lower()) for h in headers]
    # шукати щось, що містить 'lat' (латинкою) або 'лат' (кирилицею) або 'піб_лат' тощо
    for orig, low in norm:
        if "lat" in low or "лат" in low:
            return orig
    # якщо не знайшли — шукати 'pib' або 'пib_lat' варіанти
    for orig, low in norm:
        if "pib" in low or "піб" in low:
            return orig
    return None

def load_existing_filenames(html_dir):
    try:
        files = os.listdir(html_dir)
    except FileNotFoundError:
        return []
    # тільки імена без розширення
    return [os.path.splitext(f)[0] for f in files if f.lower().endswith(".html")]

def main():
    if not os.path.exists(CSV_FILE):
        print(f"[err] Не знайдено {CSV_FILE} у поточній папці: {os.getcwd()}")
        sys.exit(1)

    delimiter = detect_delimiter(CSV_FILE)
    print(f"[info] Визначено роздільник: '{delimiter}'")

    # читаємо CSV заголовки
    with open(CSV_FILE, encoding="utf-8-sig", errors="replace") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            headers = next(reader)
        except StopIteration:
            print("[err] CSV порожній")
            sys.exit(1)

    lat_col = find_lat_column(headers)
    if not lat_col:
        print("[err] Не вдалося знайти колонку з латинізованим іменем (шукаю 'lat' або 'лат' у заголовках).")
        print("Headers:", headers)
        sys.exit(1)

    # Перечитуємо CSV як DictReader із знайденим заголовком
    with open(CSV_FILE, encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        total = 0
        found = []
        missing = []
        existing_names = load_existing_filenames(HTML_DIR)

        for row in reader:
            total += 1
            # беремо значення колонки (ключ у DictReader точно такий, як у headers)
            pib_lat = row.get(lat_col) or row.get(lat_col.strip()) or ""
            pib_lat = pib_lat.strip()
            if not pib_lat:
                # якщо порожній — пропускаємо
                continue

            # нормалізація: прибираємо пробіли, подвійні підкреслення тощо
            filename = pib_lat.replace(" ", "_").strip()
            html_path = os.path.join(HTML_DIR, f"{filename}.html")

            if os.path.exists(html_path):
                found.append(filename)
            else:
                missing.append(filename)

    print(f"[ok] Перевірено (рядків з ПІБ_лат): {len(found) + len(missing)} (всього рядків у csv: {total})")
    print(f"[+] Знайдено сторінок: {len(found)}")
    print(f"[-] Відсутні сторінок: {len(missing)}")

    # Запис простого списку
    with open(OUT_SIMPLE, "w", encoding="utf-8") as out:
        out.write("\n".join(m + ".html" for m in missing))

    # Пишемо файл з підказками (fuzzy match)
    suggestions = {}
    for m in missing:
        suggestions[m] = get_close_matches(m, existing_names, n=CLOSE_MATCH_N, cutoff=CLOSE_MATCH_CUTOFF)

    with open(OUT_SUGGEST, "w", encoding="utf-8") as out:
        out.write("=== Відсутні сторінки та підказки (можливі назви файлів) ===\n\n")
        for m in missing:
            out.write(f"{m}.html\n")
            sugg = suggestions.get(m, [])
            if sugg:
                out.write("  Можливі схожі файли:\n")
                for s in sugg:
                    out.write(f"    - {s}.html\n")
            else:
                out.write("  Немає схожих файлів у папці soldiers/\n")
            out.write("\n")

    print(f"\n[log] Збережено: {OUT_SIMPLE} та {OUT_SUGGEST}")
    if missing:
        print("[hint] Відкрий missing_with_suggestions.txt щоб побачити можливі відповідники (наприклад, 'slizovskyi...' vs 'slizovskyy...').")
    else:
        print("[ok] Усі сторінки присутні (або немає рядків з ПІБ_лат).")

if __name__ == "__main__":
    main()
