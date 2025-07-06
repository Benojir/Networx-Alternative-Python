@echo off
SETLOCAL EnableDelayedExpansion

:: =============================================
:: SpeedMeter Professional Installer
:: Version 1.0
:: =============================================

:: Admin Check (Comment out if user-level install)
:: net session >nul 2>&1 || (echo Please run as Administrator! && pause && exit /b 1)

:: Configuration
set APP_NAME=SpeedMeter
set APP_EXE=SpeedMeterApp.exe
set APP_ICON=speedmeter.ico
set INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%
set SHORTCUT_NAME=%APP_NAME%.lnk

:: Colors
set RED=31
set GREEN=32
set YELLOW=33
set ESC=[

:: Header
echo %ESC%[%GREEN%m
echo === %APP_NAME% Installation ===
echo %ESC%[0m

:: Step 1: Create Installation Directory
echo %ESC%[%YELLOW%m[1/4] Creating directories...%ESC%[0m
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if errorlevel 1 (
        echo %ESC%[%RED%mError: Failed to create installation directory%ESC%[0m
        exit /b 1
    )
)

:: Step 2: Copy Files
echo %ESC%[%YELLOW%m[2/4] Installing files...%ESC%[0m
copy "%APP_EXE%" "%INSTALL_DIR%\" >nul
copy "%APP_ICON%" "%INSTALL_DIR%\" >nul

if not exist "%INSTALL_DIR%\%APP_EXE%" (
    echo %ESC%[%RED%mError: Failed to copy application files%ESC%[0m
    exit /b 1
)

:: Step 3: Create Start Menu Shortcut
echo %ESC%[%YELLOW%m[3/4] Creating shortcuts...%ESC%[0m
powershell -NoProfile -Command "\
    $s = (New-Object -COM WScript.Shell).CreateShortcut('$env:APPDATA\Microsoft\Windows\Start Menu\Programs\%SHORTCUT_NAME%');\
    $s.TargetPath = '%INSTALL_DIR%\%APP_EXE%';\
    $s.IconLocation = '%INSTALL_DIR%\%APP_ICON%,0';\
    $s.Save()"

:: Step 4: Configure Auto-Start (Multiple Methods)
echo %ESC%[%YELLOW%m[4/4] Configuring auto-start...%ESC%[0m

:: Method 1: Registry (User-Level)
reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /t REG_SZ /d "\"%INSTALL_DIR%\%APP_EXE%\"" /f >nul

:: Method 2: Scheduled Task (More Reliable)
schtasks /create /tn "%APP_NAME%" /tr "\"%INSTALL_DIR%\%APP_EXE%\"" /sc onlogon /ru "%USERNAME%" /rl HIGHEST /f >nul 2>&1

:: Completion Message
echo %ESC%[%GREEN%m
echo Installation Complete!
echo ----------------------
echo %ESC%[0m
echo Installed to: %INSTALL_DIR%
echo Start Menu: %APPDATA%\Microsoft\Windows\Start Menu\Programs\%SHORTCUT_NAME%
echo 
echo %ESC%[33mNote:%ESC%[0m SpeedMeter will now run automatically at Windows startup.
echo %ESC%[33mTo uninstall:%ESC%[0m Run uninstall.bat
echo %ESC%[32mPress any key to launch %APP_NAME%...%ESC%[0m
pause >nul

:: Launch Application
start "" "%INSTALL_DIR%\%APP_EXE%"

ENDLOCAL
exit /b 0