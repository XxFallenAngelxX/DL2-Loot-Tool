@echo off
REM Überprüfen, ob Python installiert ist
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python ist nicht installiert oder nicht im PATH.
    pause
    exit /b
)

REM In das Verzeichnis wechseln, in dem das Tool liegt
cd /d "%~dp0"

REM Python-Skript ausführen (LootTool.py)
python LootTool.py

REM Warten, bis der Benutzer eine Taste drückt, um das Fenster offen zu halten
echo.
echo Das Tool wurde erfolgreich ausgeführt. Drücke eine Taste, um fortzufahren.
pause >nul