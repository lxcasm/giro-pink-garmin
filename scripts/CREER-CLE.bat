@echo off
chcp 65001 >nul
setlocal

set "PROJECT=%~dp0.."
for %%I in ("%PROJECT%") do set "PROJECT=%%~fI"
set "CONFIG=%PROJECT%\config"
set "KEY=%CONFIG%\developer_key.der"
set "PEM=%CONFIG%\developer_key.pem"

echo.
echo === Cle developpeur Garmin (developer_key.der) ===
echo Projet: %PROJECT%
echo.

if exist "%KEY%" (
    echo Cle deja presente: %KEY%
    echo NE la partage jamais / pas sur GitHub.
    pause
    exit /b 0
)

if not exist "%CONFIG%" mkdir "%CONFIG%"

set "OPENSSL="
if exist "C:\Program Files\Git\usr\bin\openssl.exe" set "OPENSSL=C:\Program Files\Git\usr\bin\openssl.exe"
where openssl >nul 2>&1 && if not defined OPENSSL set "OPENSSL=openssl"

if not defined OPENSSL (
    echo OpenSSL introuvable. Installe Git for Windows.
    pause
    exit /b 1
)

"%OPENSSL%" genrsa -out "%PEM%" 4096
"%OPENSSL%" pkcs8 -topk8 -inform PEM -outform DER -in "%PEM%" -out "%KEY%" -nocrypt

echo OK -> %KEY%
pause
