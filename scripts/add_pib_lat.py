import csv

INPUT = "bmz.csv"
OUTPUT = "bmz.csv"

def translit(name):
    table = str.maketrans({
        'А':'A','Б':'B','В':'V','Г':'H','Ґ':'G','Д':'D','Е':'E','Є':'Ye','Ж':'Zh','З':'Z',
        'И':'Y','І':'I','Ї':'Yi','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P',
        'Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Shch',
        'Ю':'Yu','Я':'Ya','Ь':'','’':'','\'':'',
        'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','ж':'zh','з':'z',
        'и':'y','і':'i','ї':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p',
        'р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch',
        'ю':'iu','я':'ia','ь':'',' ':'_'
    })
    return name.translate(table).lower()

rows = []
with open(INPUT, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    fieldnames = reader.fieldnames + (['ПІБ_лат'] if 'ПІБ_лат' not in reader.fieldnames else [])
    for row in reader:
        row['ПІБ_лат'] = translit(row['ПІБ'])
        rows.append(row)

with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)

print(f"[ok] Оновлено {OUTPUT} — усі ПІБ_лат синхронізовані ({len(rows)} записів)")
