@echo off
setlocal

rem M2EX validates ownership through Steam. Start the client when it is not
rem already running, then launch from the Medieval II root while keeping the
rem executable and its 64-bit runtime files together in the mod directory.
tasklist /FI "IMAGENAME eq steam.exe" 2>nul | find /I "steam.exe" >nul
if errorlevel 1 (
    echo Starting Steam...
    start "" "steam://open/main"
    for /L %%I in (1,1,30) do (
        timeout /t 1 /nobreak >nul
        tasklist /FI "IMAGENAME eq steam.exe" 2>nul | find /I "steam.exe" >nul && goto steam_started
    )
)

:steam_started
cd /d "%~dp0..\.."
start "" "%~dp0SteamAndSteel.exe" @mods\steamsteel\steamsteel.cfg
endlocal
