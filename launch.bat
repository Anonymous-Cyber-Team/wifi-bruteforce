@echo off
title WiFi Bruteforcer Suite
color 0A

echo.
echo  ============================================
echo   WiFi Bruteforcer Suite - Windows Edition
echo   Based on: faizann24/wifi-bruteforcer-fsecurify
echo  ============================================
echo.
echo  [1] WiFi Bruteforcer (Main Tool)
echo  [2] Wordlist Generator
echo  [3] Exit
echo.
set /p choice="  Select option (1/2/3): "

if "%choice%"=="1" goto bruteforcer
if "%choice%"=="2" goto generator
if "%choice%"=="3" goto exit_app
goto menu

:bruteforcer
echo.
echo  Starting WiFi Bruteforcer...
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0wifi_bruteforcer.py"
goto end

:generator
echo.
echo  Starting Wordlist Generator...
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0wordlist_generator.py"
goto end

:exit_app
echo  Goodbye!
exit /b 0

:end
pause
