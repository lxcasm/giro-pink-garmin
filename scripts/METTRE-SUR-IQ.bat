@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "PROJECT=%~dp0.."
for %%I in ("%PROJECT%") do set "PROJECT=%%~fI"
set "TOOLS=D:\logiciel que cursor a instalée\Garmin-ConnectIQ"
set "CLI=%TOOLS%\tools\connect-iq-sdk-manager.exe"
set "OUT=%PROJECT%\bin\GiroPink.prg"
set "KEY=%PROJECT%\config\developer_key.der"

echo.
echo === Giro Pink - Edge 1040 (copie sur l'appareil) ===
echo.

if exist "%CLI%" (
    "%CLI%" agreement accept >nul 2>&1
    "%CLI%" device download -d edge1040 2>nul
)

if not exist "%KEY%" call "%~dp0CREER-CLE.bat"

call "%~dp0_find-monkeyc.bat" || exit /b 1

if not exist "%PROJECT%\bin" mkdir "%PROJECT%\bin"

pushd "%PROJECT%"
call "!MONKEYC!" -f monkey.jungle -o "%OUT%" -y "%KEY%" -d edge1040 -w -e
set "ERR=!ERRORLEVEL!"
popd

if !ERR! neq 0 ( pause & exit /b !ERR! )

echo OK -> %OUT%
for %%D in (E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%D:\GARMIN\APPS" copy /Y "%OUT%" "%%D:\GARMIN\APPS\GiroPink.prg"
)
pause
