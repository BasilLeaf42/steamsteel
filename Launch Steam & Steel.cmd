@echo off
setlocal

rem The tow_steamsteel tree is the authoritative runtime overlay.  Apply it
rem before every launch so developer installs and upgraded releases cannot run
rem stale copies from data\.
set "MODDIR=%~dp0"
if exist "%MODDIR%data\tow_steamsteel" (
    robocopy "%MODDIR%data\tow_steamsteel" "%MODDIR%data" /E /COPY:DAT /DCOPY:DAT /R:2 /W:1 /NFL /NDL /NJH /NJS /NP >nul
    if errorlevel 8 (
        echo Steam ^& Steel could not apply its authoritative data overlay.
        echo Close editors using the mod files, then try again.
        pause
        exit /b 1
    )
)

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
