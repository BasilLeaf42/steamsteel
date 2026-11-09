Option Explicit

Dim shell, files, modDir, gameDir, overlayDir, gameExe, steamExe, command, exitCode, waitCount
Set shell = CreateObject("WScript.Shell")
Set files = CreateObject("Scripting.FileSystemObject")

modDir = files.GetParentFolderName(WScript.ScriptFullName)
gameDir = files.GetParentFolderName(files.GetParentFolderName(modDir))
overlayDir = files.BuildPath(modDir, "data\tow_steamsteel")
gameExe = files.BuildPath(gameDir, "SteamAndSteel.exe")

' Apply the authoritative runtime overlay without opening a console window.
If files.FolderExists(overlayDir) Then
    command = "robocopy """ & overlayDir & """ """ & files.BuildPath(modDir, "data") & _
              """ /E /COPY:DAT /DCOPY:DAT /R:2 /W:1 /NFL /NDL /NJH /NJS /NP"
    exitCode = shell.Run(command, 0, True)
    If exitCode >= 8 Then
        MsgBox "Steam & Steel could not apply its authoritative data overlay." & vbCrLf & _
               "Close editors using the mod files, then try again.", vbCritical, "Steam & Steel"
        WScript.Quit 1
    End If
End If

' Start Steam only when it is not already running.
If Not IsProcessRunning("steam.exe") Then
    steamExe = ReadSteamPath()
    If steamExe <> "" And files.FileExists(steamExe) Then
        shell.Run """" & steamExe & """ -silent", 0, False
    Else
        shell.Run "steam://open/main", 0, False
    End If

    For waitCount = 1 To 90
        If IsProcessRunning("steam.exe") Then Exit For
        WScript.Sleep 1000
    Next
End If

If Not files.FileExists(gameExe) Then
    MsgBox "Steam & Steel could not find its branded game executable.", vbCritical, "Steam & Steel"
    WScript.Quit 1
End If

shell.CurrentDirectory = gameDir
shell.Run """" & gameExe & """ ""@mods\steamsteel\steamsteel.cfg"" --features.mod=mods/steamsteel", 1, False

Function IsProcessRunning(processName)
    Dim service, processes
    Set service = GetObject("winmgmts:\\.\root\cimv2")
    Set processes = service.ExecQuery("Select * From Win32_Process Where Name='" & processName & "'")
    IsProcessRunning = (processes.Count > 0)
End Function

Function ReadSteamPath()
    On Error Resume Next
    ReadSteamPath = shell.RegRead("HKCU\Software\Valve\Steam\SteamExe")
    If Err.Number <> 0 Then
        Err.Clear
        ReadSteamPath = ""
    End If
    On Error GoTo 0

    If ReadSteamPath = "" Then
        If files.FileExists(shell.ExpandEnvironmentStrings("%ProgramFiles(x86)%\Steam\steam.exe")) Then
            ReadSteamPath = shell.ExpandEnvironmentStrings("%ProgramFiles(x86)%\Steam\steam.exe")
        ElseIf files.FileExists(shell.ExpandEnvironmentStrings("%ProgramFiles%\Steam\steam.exe")) Then
            ReadSteamPath = shell.ExpandEnvironmentStrings("%ProgramFiles%\Steam\steam.exe")
        End If
    End If
End Function
