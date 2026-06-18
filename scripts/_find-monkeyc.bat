@echo off
set "TOOLS=D:\logiciel que cursor a instalée\Garmin-ConnectIQ"
set "SDK=%TOOLS%\ConnectIQ\Sdks"
set "MONKEYC="

for /d %%S in ("%SDK%\connectiq-sdk-*") do (
    if exist "%%S\bin\monkeyc.bat" set "MONKEYC=%%S\bin\monkeyc.bat"
)
if not defined MONKEYC if exist "%SDK%\bin\monkeyc.bat" set "MONKEYC=%SDK%\bin\monkeyc.bat"

if not defined MONKEYC (
    echo SDK Garmin introuvable: %TOOLS%
    exit /b 1
)
exit /b 0
