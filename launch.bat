@echo off
title Devil-X WiFi Bruteforce 2.0
color 0B

:menu
cls
echo.
echo  ======================================================
echo     DEVIL-X WIFI BRUTEFORCE 2.0 -- CYBER SUITE
echo     Developer: MD Shamim ^| Devil-X Studios
echo  ======================================================
echo.
echo  [1] WiFi Bruteforcer (GUI Attack Tool)
echo  [2] Wordlist Generator (Custom Dictionary Maker)
echo  [3] License & Hash Generator (Browser Tool)
echo  [4] Exit
echo.
set /p choice="  Select option (1/2/3/4): "

if "%choice%"=="1" goto bruteforcer
if "%choice%"=="2" goto generator
if "%choice%"=="3" goto hashtool
if "%choice%"=="4" goto exit_app
goto menu

:bruteforcer
echo.
echo  Starting Devil-X WiFi Bruteforcer...
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0wifi_bruteforcer.py"
goto end

:generator
echo.
echo  Starting Devil-X Wordlist Generator...
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0wordlist_generator.py"
goto end

:hashtool
echo.
echo  Opening Devil-X Hash & License Generator...
start "" "%~dp0tools\hash_generator.html"
goto menu

:exit_app
echo  Exiting Devil-X Suite...
exit /b 0

:end
pause

