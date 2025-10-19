@echo off
:: === Автоматичне оновлення сайту БМЗ ===
cd /d "%~dp0"

echo.
echo ============================================
echo   🔄  BMZ AUTO-UPDATE START
echo ============================================
echo.

:: Крок 1 — Оновлення репозиторію
echo [1/4] Отримання останніх змін з GitHub...
git pull origin main

:: Крок 2 — Генерація сторінок військовослужбовців
echo.
echo [2/4] Генерація soldier profiles...
python scripts\generate_profiles.py

:: Крок 3 — Додавання і коміт змін
echo.
echo [3/4] Підготовка до пушу...
git add .
git commit -m "auto: daily update %date% %time%" >NUL 2>&1

:: Крок 4 — Публікація на GitHub
echo.
echo [4/4] Відправлення оновлень на GitHub...
git push origin main

echo.
echo ✅ Оновлення завершено успішно!
echo.
pause
