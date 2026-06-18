@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "PROJECT=%~dp0.."
for %%I in ("%PROJECT%") do set "PROJECT=%%~fI"
set "KEY=%PROJECT%\config\developer_key.der"
set "OUT=%PROJECT%\bin\GiroPink.iq"

echo.
echo === Build .IQ (publication Connect IQ Store) ===
echo.

if not exist "%KEY%" (
    echo Cle manquante. Lance CREER-CLE.bat
    pause
    exit /b 1
)

call "%~dp0_find-monkeyc.bat" || exit /b 1

if not exist "%PROJECT%\bin" mkdir "%PROJECT%\bin"

pushd "%PROJECT%"
call "!MONKEYC!" -f monkey.jungle -o "%OUT%" -y "%KEY%" -d edge1040 -w -e
set "ERR=!ERRORLEVEL!"
popd

if !ERR! neq 0 ( pause & exit /b !ERR! )
echo Fichier: %OUT%
pause
