@echo off
SETLOCAL EnableDelayedExpansion

:: =============================================
:: SpeedMeter Professional Uninstaller
:: Version 1.0
:: =============================================

:: Configuration
set APP_NAME=SpeedMeter
set APP_EXE=SpeedMeterApp.exe
set INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%
set SHORTCUT_NAME=%APP_NAME%.lnk

:: Colors (for console output)
set RED=31
set GREEN=32
set YELLOW=33
set ESC=[

:: Header
echo %ESC%[%GREEN%m
echo === %APP_NAME% Removal ===
echo %ESC%[0m

:: Step 1: Stop Running Process
echo %ESC%[%YELLOW%m[1/4] Stopping running instances...%ESC%[0m
taskkill /f /im "%APP_EXE%" >nul 2>&1
timeout /t 2 /nobreak >nul

:: Step 2: Remove Auto-Start Entries
echo %ESC%[%YELLOW%m[2/4] Removing startup entries...%ESC%[0m

:: Remove Registry Entry
reg delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /f >nul 2>&1

:: Remove Scheduled Task
schtasks /delete /tn "%APP_NAME%" /f >nul 2>&1

:: Remove Startup Folder Shortcut (if exists)
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\%SHORTCUT_NAME%" >nul 2>&1

:: Step 3: Remove Shortcuts
echo %ESC%[%YELLOW%m[3/4] Removing shortcuts...%ESC%[0m
del "%USERPROFILE%\Desktop\%SHORTCUT_NAME%" >nul 2>&1
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\%SHORTCUT_NAME%" >nul 2>&1

:: Step 4: Remove Installation Directory
echo %ESC%[%YELLOW%m[4/4] Removing files...%ESC%[0m
if exist "%INSTALL_DIR%" (
    rd /s /q "%INSTALL_DIR%" >nul 2>&1
    if exist "%INSTALL_DIR%" (
        echo %ESC%[%RED%mWarning: Could not fully remove installation directory%ESC%[0m
        echo You may need to manually delete: %INSTALL_DIR%
    )
)

:: Completion Message
echo %ESC%[%GREEN%m
echo Uninstallation Complete!
echo -----------------------
echo %ESC%[0m
echo All %APP_NAME% components have been removed from:
echo - Startup entries
echo - Program files
echo - Shortcuts
echo.
echo %ESC%[32mNote:%ESC%[0m Some files may remain in use until next reboot.
echo %ESC%[32mPress any key to exit...%ESC%[0m
pause >nul

ENDLOCAL
exit /b 0