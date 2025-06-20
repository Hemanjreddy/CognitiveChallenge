@echo off
title Mercedes-Benz MF4 Detector Installer
echo ====================================================
echo Mercedes-Benz MF4 Signal Peak Detector - Installer
echo ====================================================
echo.

set INSTALL_DIR=%USERPROFILE%\Mercedes_Benz_MF4_Detector

echo Installing to: %INSTALL_DIR%
echo.

if exist "%INSTALL_DIR%" (
    echo Removing existing installation...
    rmdir /s /q "%INSTALL_DIR%"
)

echo Creating installation directory...
mkdir "%INSTALL_DIR%"

echo Copying application files...
xcopy /s /e /y Mercedes_Benz_MF4_Detector_Portable\* "%INSTALL_DIR%\"

echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Mercedes-Benz MF4 Detector.lnk
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\start_detector.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Mercedes-Benz MF4 Signal Peak Detector'; $Shortcut.Save()"

echo.
echo ====================================================
echo Installation complete!
echo.
echo Application installed to: %INSTALL_DIR%
echo Desktop shortcut created: Mercedes-Benz MF4 Detector
echo.
echo To start the application:
echo 1. Double-click the desktop shortcut, or
echo 2. Run: %INSTALL_DIR%\start_detector.bat
echo ====================================================

pause
