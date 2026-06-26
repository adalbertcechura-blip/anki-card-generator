@echo off
echo ==================================================
echo   Spoustec Generatoru Anki Karticek
echo ==================================================
echo.

:: Kontrola Pythonu
python --version >nul 2>&1
if errorlevel 1 (
    echo [CHYBA] Python neni nainstalovan nebo neni v systemove ceste PATH!
    echo Prosim nainstalujte Python a zaskrtnete volbu pridani do PATH.
    pause
    exit /b
)

:: Aktivace nebo vytvoreni venv
if not exist venv (
    echo [INFO] Vytvarim virtualni prostredi venv...
    python -m venv venv
    if errorlevel 1 (
        echo [CHYBA] Nepodarilo se vytvorit venv!
        pause
        exit /b
    )
)

echo [INFO] Aktivuji virtualni prostredi...
call venv\Scripts\activate.bat

echo [INFO] Kontrola a instalace zavislosti...
pip install -r requirements.txt
if errorlevel 1 (
    echo [CHYBA] Selhala instalace zavislosti z requirements.txt!
    pause
    exit /b
)

echo.
echo [INFO] Spoustim aplikaci...
echo [INFO] Otevri prohlizec na adrese http://localhost:8501
echo.
streamlit run app.py

pause
