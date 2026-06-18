@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "PROJECT=%~dp0.."
for %%I in ("%PROJECT%") do set "PROJECT=%%~fI"
set "OUT=%PROJECT%\bin\GiroPink.prg"
set "KEY=%PROJECT%\config\developer_key.der"

if not exist "%KEY%" call "%~dp0CREER-CLE.bat"
call "%~dp0_find-monkeyc.bat" || exit /b 1

if not exist "%PROJECT%\bin" mkdir "%PROJECT%\bin"

pushd "%PROJECT%"
call "!MONKEYC!" -f monkey.jungle -o "%OUT%" -y "%KEY%" -d edge1040 -w
popd
pause
