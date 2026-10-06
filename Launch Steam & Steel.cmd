@echo off
setlocal

rem Production launcher: start Steam when needed, then launch the mod directly.
tasklist /FI "IMAGENAME eq steam.exe" 2>nul | find /I "steam.exe" >nul
if errorlevel 1 (
    set "STEAM_EXE="
    for /f "tokens=2,*" %%A in ('reg query "HKCU\Software\Valve\Steam" /v SteamExe 2^>nul ^| find /I "SteamExe"') do set "STEAM_EXE=%%B"
    if not defined STEAM_EXE if exist "%ProgramFiles(x86)%\Steam\steam.exe" set "STEAM_EXE=%ProgramFiles(x86)%\Steam\steam.exe"
    if not defined STEAM_EXE if exist "%ProgramFiles%\Steam\steam.exe" set "STEAM_EXE=%ProgramFiles%\Steam\steam.exe"
    if defined STEAM_EXE (
        start "" "%STEAM_EXE%" -silent
    ) else (
        start "" "steam://open/main"
    )
    for /L %%I in (1,1,90) do (
        timeout /t 1 /nobreak >nul
        tasklist /FI "IMAGENAME eq steam.exe" 2>nul | find /I "steam.exe" >nul && goto steam_started
    )
)

:steam_started
if not exist "%~dp0..\..\SteamAndSteel.exe" (
    echo Steam ^& Steel could not find its branded game executable.
    pause
    exit /b 1
)
cd /d "%~dp0..\.."
start "" "%~dp0..\..\SteamAndSteel.exe" --features.mod=mods/steamsteel
endlocal
