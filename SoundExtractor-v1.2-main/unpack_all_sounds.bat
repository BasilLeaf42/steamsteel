@echo off

:: For copyright and author details of the XIDX tool see the source and *.txt files 
:: in the XIDX folder.

:: Copyright (C) 2012  Withwnar <http://www.twcenter.net/forums/member.php?u=45403>
:: 
:: This program is free software; you can redistribute it and/or 
:: modify it under the terms of the GNU General Public License 
:: as published by the Free Software Foundation; either version 2 
:: of the License, or (at your option) any later version.
:: 
:: This program is distributed in the hope that it will be useful, 
:: but WITHOUT ANY WARRANTY; without even the implied warranty of 
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
:: GNU General Public License for more details.
:: 
:: You should have received a copy of the GNU General Public License 
:: along with this program; if not, write to the Free Software 
:: Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

:: for Vista, Win7, etc.
chdir %~dp0

:: This should be running from the SoundExtractor subfolder of the root mod folder
cd ..

if not exist data\sounds goto :WRONGDIR

set extractList=data\sounds\music data\sounds\sfx
if exist data\sounds\voice.dat set extractList=%extractList% data\sounds\voice
if exist data\sounds\voice1.dat set extractList=%extractList% data\sounds\voice1
if exist data\sounds\voice2.dat set extractList=%extractList% data\sounds\voice2
if exist data\sounds\voice3.dat set extractList=%extractList% data\sounds\voice3

.\SoundExtractor\XIDX\bin\xidx_x86.exe -x %extractList%

:: backup the idx/dat files
cd data\sounds
echo.
echo Moving all IDX/DAT files to backup folder...
set backupDate=%DATE:/=%
set backupTime=%TIME::=%
set backupDir="backup_%backupDate%_%backupTime%"
md %backupDir%
move *.idx %backupDir%
move *.dat %backupDir%

:SUCCESS
echo.
echo All done!
goto :END

:WRONGDIR
echo FAILED: this batch file must be run from the "SoundExtractor" folder which 
echo should be directly under the TATW folder. 
echo i.e. The batch file should be located here...
echo {M2TW install folder}\mods\{mod name}\SoundExtractor\extract_all_sounds.bat
echo ... or, for vanilla M2TW, here...
echo {M2TW install folder}\SoundExtractor\extract_all_sounds.bat
goto :END

:END
echo.
pause
