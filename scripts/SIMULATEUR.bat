@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "PROJECT=%~dp0.."
for %%I in ("%PROJECT%") do set "PROJECT=%%~fI"
set "OUT=%PROJECT%\bin\GiroPink.prg"
set "KEY=%PROJECT%\config\developer_key.der"

echo.
echo === Giro Pink - Simulateur Connect IQ (Edge 1040) ===
echo.

if not exist "%KEY%" call "%~dp0CREER-CLE.bat"
call "%~dp0_find-monkeyc.bat" || exit /b 1

rem -- dossier bin du SDK (la se trouvent connectiq.bat et monkeydo.bat) --
for %%F in ("!MONKEYC!") do set "SDKBIN=%%~dpF"

if not exist "%PROJECT%\bin" mkdir "%PROJECT%\bin"

echo [1/3] Compilation...
pushd "%PROJECT%"
call "!MONKEYC!" -f monkey.jungle -o "%OUT%" -y "%KEY%" -d edge1040 -w
set "ERR=!ERRORLEVEL!"
popd
if !ERR! neq 0 ( echo Echec compilation. & pause & exit /b !ERR! )

echo [2/3] Demarrage du simulateur...
start "" "!SDKBIN!connectiq.bat"

echo     (attente du demarrage du simulateur)
timeout /t 6 /nobreak >nul

echo [3/3] Chargement de l'application dans le simulateur...
call "!SDKBIN!monkeydo.bat" "%OUT%" edge1040

echo.
echo Si rien ne s'affiche, laisse le simulateur finir de demarrer
echo puis relance uniquement cette etape :
echo     "!SDKBIN!monkeydo.bat" "%OUT%" edge1040
echo.
pause
