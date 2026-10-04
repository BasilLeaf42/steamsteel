#ifndef MyAppVersion
  #define MyAppVersion "prerelease"
#endif
#ifndef MusicDatBytes
  #define MusicDatBytes 1006556167
#endif
#ifndef MusicIdxBytes
  #define MusicIdxBytes 22260
#endif
#ifndef SfxDatBytes
  #define SfxDatBytes 952213331
#endif
#ifndef SfxIdxBytes
  #define SfxIdxBytes 26806
#endif

[Setup]
AppId={{E120887A-E207-4C8A-B064-28A81C68A42D}
AppName=Steam & Steel
AppVersion={#MyAppVersion}
AppPublisher=Steam & Steel Development Team
DefaultDirName={code:GetDefaultGameDirectory}
DefaultGroupName=Steam & Steel
DisableProgramGroupPage=yes
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=Steam_and_Steel_Setup
SetupIconFile=payload\steamsteel\steamateelicon.ico
UninstallDisplayIcon={app}\mods\steamsteel\SteamAndSteel.exe
WizardStyle=modern
WizardSizePercent=110
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
Compression=lzma2/ultra64
SolidCompression=yes
CloseApplications=yes
RestartApplications=no
UsePreviousAppDir=yes
DirExistsWarning=no
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{src}\payload\steamsteel\*"; DestDir: "{app}\mods\steamsteel"; Flags: external ignoreversion recursesubdirs createallsubdirs
; M2EX paths are selected from the verified upstream distribution, but their
; bytes come from the maintainer's current installed root so deliberate local
; fixes and other developers' deviations are preserved in the release.
Source: "{src}\payload\m2ex_root\*"; DestDir: "{app}"; Flags: external ignoreversion recursesubdirs createallsubdirs uninsneveruninstall
; Also install the verified graphics configuration into the mod override tree.
; M2EX normally resolves the game-root copy, but this removes dependence on
; fallback resolution and prevents the startup CTD seen on some clean installs.
Source: "{src}\payload\m2ex_root\data\graphics\graphics_config.xml"; DestDir: "{app}\mods\steamsteel\data\graphics"; Flags: external ignoreversion
Source: "{src}\payload\m2ex_root\steam_api64.dll"; DestDir: "{app}\mods\steamsteel"; Flags: external ignoreversion
Source: "{src}\payload\m2ex_root\mss64.dll"; DestDir: "{app}\mods\steamsteel"; Flags: external ignoreversion
Source: "{src}\payload\m2ex_root\binkw64.dll"; DestDir: "{app}\mods\steamsteel"; Flags: external ignoreversion
Source: "{src}\payload\m2ex_root\granny2_x64.dll"; DestDir: "{app}\mods\steamsteel"; Flags: external ignoreversion
Source: "{src}\payload\m2ex_root\steam_appid.txt"; DestDir: "{app}\mods\steamsteel"; Flags: external ignoreversion
Source: "{src}\payload\prerequisites\vc_redist.x64.exe"; DestDir: "{tmp}"; Flags: external deleteafterinstall

[Icons]
Name: "{autoprograms}\Steam & Steel"; Filename: "{app}\mods\steamsteel\Launch Steam & Steel.cmd"; WorkingDir: "{app}"; IconFilename: "{app}\mods\steamsteel\steamateelicon.ico"
Name: "{autodesktop}\Steam & Steel"; Filename: "{app}\mods\steamsteel\Launch Steam & Steel.cmd"; WorkingDir: "{app}"; IconFilename: "{app}\mods\steamsteel\steamateelicon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked

[Run]
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/install /passive /norestart"; StatusMsg: "Installing the Microsoft Visual C++ runtime..."; Flags: waituntilterminated skipifdoesntexist
Filename: "{app}\mods\steamsteel\Launch Steam & Steel.cmd"; Description: "Launch Steam & Steel"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent shellexec
Filename: "{cmd}"; Parameters: "/C timeout /t 4 /nobreak >nul 2>&1 & rmdir /s /q ""{src}\payload"" & del /f /q ""{srcexe}"" & del /f /q ""{src}\Steam_and_Steel_{#MyAppVersion}.7z"""; WorkingDir: "{tmp}"; Description: "Remove extracted installation files and the same-folder release archive"; Flags: nowait postinstall runhidden skipifsilent unchecked

[Code]
var
  DetectedGameDirectory: string;
  ExistingInstallPurgeConfirmed: Boolean;

function GetSteamSteelDirectory: string;
begin
  Result := AddBackslash(RemoveBackslashUnlessRoot(WizardDirValue)) + 'mods\steamsteel';
end;

function IsCompatibleGameDirectory(const Candidate: string): Boolean;
begin
  Result := FileExists(AddBackslash(Candidate) + 'medieval2.exe') and
            DirExists(AddBackslash(Candidate) + 'data');
end;

function TryCandidate(const Candidate: string): Boolean;
var
  Expanded: string;
begin
  Expanded := RemoveBackslashUnlessRoot(ExpandConstant(Candidate));
  Result := IsCompatibleGameDirectory(Expanded);
  if Result then
    DetectedGameDirectory := Expanded;
end;

function ExtractVdfPath(Line: string): string;
var
  MarkerPos, OpenQuote, CloseQuote: Integer;
begin
  Result := '';
  MarkerPos := Pos('"path"', Lowercase(Line));
  if MarkerPos = 0 then Exit;
  Delete(Line, 1, MarkerPos + 5);
  OpenQuote := Pos('"', Line);
  if OpenQuote = 0 then Exit;
  Delete(Line, 1, OpenQuote);
  CloseQuote := Pos('"', Line);
  if CloseQuote = 0 then Exit;
  Result := Copy(Line, 1, CloseQuote - 1);
  StringChangeEx(Result, '\\', '\', True);
end;

function DetectSteamLibraries(const SteamPath: string): Boolean;
var
  Lines: TArrayOfString;
  I: Integer;
  LibraryPath, LibrariesFile: string;
begin
  Result := False;
  LibrariesFile := AddBackslash(SteamPath) + 'steamapps\libraryfolders.vdf';
  if not LoadStringsFromFile(LibrariesFile, Lines) then Exit;
  for I := 0 to GetArrayLength(Lines) - 1 do
  begin
    LibraryPath := ExtractVdfPath(Lines[I]);
    if (LibraryPath <> '') and
       TryCandidate(AddBackslash(LibraryPath) + 'steamapps\common\Medieval II Total War') then
    begin
      Result := True;
      Exit;
    end;
  end;
end;

function DetectSteamDefault: Boolean;
var
  SteamPath: string;
begin
  Result := False;
  if RegQueryStringValue(HKLM32,
       'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 4700',
       'InstallLocation', SteamPath) and TryCandidate(SteamPath) then
  begin
    Result := True;
    Exit;
  end;
  if RegQueryStringValue(HKCU, 'Software\Valve\Steam', 'SteamPath', SteamPath) and
     (TryCandidate(AddBackslash(SteamPath) + 'steamapps\common\Medieval II Total War') or
      DetectSteamLibraries(SteamPath)) then
  begin
    Result := True;
    Exit;
  end;
  if TryCandidate('{pf32}\Steam\steamapps\common\Medieval II Total War') then
  begin
    Result := True;
    Exit;
  end;
  if TryCandidate('{pf}\Steam\steamapps\common\Medieval II Total War') then
  begin
    Result := True;
    Exit;
  end;
  if TryCandidate('{src}') or TryCandidate(ExtractFileDir(ExpandConstant('{src}'))) then
    Result := True;
end;

function GetDefaultGameDirectory(Param: string): string;
begin
  if DetectedGameDirectory = '' then
    DetectSteamDefault;
  if DetectedGameDirectory <> '' then
    Result := DetectedGameDirectory
  else
    Result := ExpandConstant('{pf32}\Steam\steamapps\common\Medieval II Total War');
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  ExistingDirectory: string;
begin
  Result := True;
  if CurPageID = wpSelectDir then
  begin
    if not IsCompatibleGameDirectory(WizardDirValue) then
    begin
      MsgBox(
        'Select the Medieval II: Total War installation folder itself.' + #13#10 + #13#10 +
        'The selected folder must contain medieval2.exe and the data folder. Do not select the mods folder.',
        mbError, MB_OK);
      Result := False;
    end;
  end;
  if (CurPageID = wpReady) then
  begin
    ExistingDirectory := GetSteamSteelDirectory;
    if DirExists(ExistingDirectory) and not ExistingInstallPurgeConfirmed then
    begin
      if MsgBox(
        'A Steam & Steel folder already exists:' + #13#10 + #13#10 +
        ExistingDirectory + #13#10 + #13#10 +
        'To prevent obsolete or incompatible files from surviving the upgrade, setup must permanently delete the entire existing Steam & Steel folder before installing this release.' + #13#10 + #13#10 +
        'This also removes saves, preferences, backups, and personal files stored inside that folder. Copy anything you want to keep elsewhere before continuing.' + #13#10 + #13#10 +
        'Delete the existing folder and continue?',
        mbConfirmation, MB_YESNO) <> IDYES then
      begin
        Result := False;
        Exit;
      end;
      ExistingInstallPurgeConfirmed := True;
    end;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ExistingDirectory: string;
begin
  Result := '';
  ExistingDirectory := GetSteamSteelDirectory;

  if DirExists(ExistingDirectory) then
  begin
    if not ExistingInstallPurgeConfirmed then
    begin
      Result := 'Setup cannot overwrite an existing Steam & Steel installation without explicit approval to purge it. Run setup interactively and confirm the clean installation.';
      Exit;
    end;

    if not IsCompatibleGameDirectory(WizardDirValue) then
    begin
      Result := 'The selected Medieval II installation could not be validated immediately before cleanup. No files were removed.';
      Exit;
    end;

    if not DelTree(ExistingDirectory, True, True, True) then
    begin
      Result := 'Setup could not completely remove the existing Steam & Steel folder. Close the game, launcher, editors, and file-browser windows using the folder, then try again.';
      Exit;
    end;
  end;
end;

procedure InitializeWizard;
begin
  ExistingInstallPurgeConfirmed := False;
  WizardForm.WelcomeLabel2.Caption :=
    'This installer adds Steam & Steel to an existing Medieval II: Total War installation.' + #13#10 + #13#10 +
    'The game folder is detected automatically when possible. A non-standard installation can be selected manually.' + #13#10 + #13#10 +
    'Clean-install notice: if mods\steamsteel already exists, setup will ask permission to delete that entire folder before installation. Back up any saves or personal files you want to retain.';
end;

procedure RequireInstalledFile(const RelativePath: string; ExpectedBytes: Int64);
var
  InstalledPath: string;
  ActualBytes: Int64;
begin
  InstalledPath := AddBackslash(WizardDirValue) + 'mods\steamsteel\' + RelativePath;
  if (not FileSize64(InstalledPath, ActualBytes)) or (ActualBytes <> ExpectedBytes) then
    RaiseException(
      'Installation validation failed for ' + RelativePath + '.' + #13#10 +
      'The release was incomplete or damaged. Re-extract the full download and run setup again.');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    RequireInstalledFile('data\sounds\Music.dat', {#MusicDatBytes});
    RequireInstalledFile('data\sounds\Music.idx', {#MusicIdxBytes});
    RequireInstalledFile('data\sounds\SFX.dat', {#SfxDatBytes});
    RequireInstalledFile('data\sounds\SFX.idx', {#SfxIdxBytes});
    RequireInstalledFile('data\unit_models\_units\bnw\textures\jap_navewuqi.texture', 1398304);
    RequireInstalledFile('data\battlefield\fire\smoke6_greek.texture', 22048);
    RequireInstalledFile('data\battlefield\fire\greek_burning_smoke.texture', 22048);
  end;
end;
