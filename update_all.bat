@echo off
cd /d "%~dp0"
echo ==========================================
echo 🔄  BMZ PLANER: автоматичне оновлення GitHub
echo ==========================================
echo.
git add -A
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set mydate=%%d-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set mytime=%%a:%%b
git commit -m "auto update %mydate% %mytime%"
git push origin main
echo.
echo ✅ Оновлення завершено.
echo Натисніть будь-яку клавішу для виходу...
pause >nul
