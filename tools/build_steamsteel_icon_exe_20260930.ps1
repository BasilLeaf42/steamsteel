$ErrorActionPreference = 'Stop'

$sourceExe = Resolve-Path '..\..\M2EX.exe'
$targetExe = Join-Path (Resolve-Path '.').Path 'M2EX.exe'
$iconPath = Resolve-Path 'steamateelicon.ico'

Copy-Item -LiteralPath $sourceExe -Destination $targetExe -Force

Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class ResourceUpdate {
    [DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
    public static extern IntPtr BeginUpdateResource(string file, bool deleteExistingResources);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool UpdateResource(IntPtr handle, IntPtr type, IntPtr name, ushort language, byte[] data, uint size);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool EndUpdateResource(IntPtr handle, bool discard);
}
'@

$ico = [System.IO.File]::ReadAllBytes($iconPath)
$count = [BitConverter]::ToUInt16($ico, 4)
if ($count -lt 1) { throw 'The ICO contains no image entries.' }

$group = New-Object System.Collections.Generic.List[byte]
$group.AddRange([BitConverter]::GetBytes([uint16]0))
$group.AddRange([BitConverter]::GetBytes([uint16]1))
$group.AddRange([BitConverter]::GetBytes([uint16]$count))

$handle = [ResourceUpdate]::BeginUpdateResource($targetExe, $false)
if ($handle -eq [IntPtr]::Zero) { throw "BeginUpdateResource failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }

try {
    for ($i = 0; $i -lt $count; $i++) {
        $entry = 6 + (16 * $i)
        $bytesInImage = [BitConverter]::ToUInt32($ico, $entry + 8)
        $imageOffset = [BitConverter]::ToUInt32($ico, $entry + 12)
        $image = New-Object byte[] $bytesInImage
        [Array]::Copy($ico, $imageOffset, $image, 0, $bytesInImage)
        $iconId = [uint16](201 + $i)
        foreach ($language in [uint16[]]@(0, 1033, 2057)) {
            if (-not [ResourceUpdate]::UpdateResource($handle, [IntPtr]3, [IntPtr]$iconId, $language, $image, $image.Length)) {
                throw "Updating icon image failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
            }
        }
        $group.AddRange([byte[]]$ico[$entry..($entry + 11)])
        $group.AddRange([BitConverter]::GetBytes($iconId))
    }
    $groupData = $group.ToArray()
    $groupResources = @(
        @{ Id = 1; Language = 0 },
        @{ Id = 101; Language = 2057 },
        @{ Id = 108; Language = 1033 },
        @{ Id = 109; Language = 1033 },
        @{ Id = 110; Language = 1033 },
        @{ Id = 111; Language = 1033 }
    )
    foreach ($resource in $groupResources) {
        if (-not [ResourceUpdate]::UpdateResource($handle, [IntPtr]14, [IntPtr]$resource.Id, [uint16]$resource.Language, $groupData, $groupData.Length)) {
            throw "Updating group icon failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
        }
    }
    if (-not [ResourceUpdate]::EndUpdateResource($handle, $false)) {
        throw "EndUpdateResource failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
    }
    $handle = [IntPtr]::Zero
}
finally {
    if ($handle -ne [IntPtr]::Zero) { [ResourceUpdate]::EndUpdateResource($handle, $true) | Out-Null }
}

function Replace-FixedUtf16String([byte[]]$Bytes, [string]$Old, [string]$New) {
    if ($New.Length -gt $Old.Length) { throw "Replacement '$New' is longer than '$Old'." }
    $oldBytes = [Text.Encoding]::Unicode.GetBytes($Old)
    $newBytes = [Text.Encoding]::Unicode.GetBytes($New.PadRight($Old.Length, [char]0))
    $replacements = 0
    for ($i = 0; $i -le $Bytes.Length - $oldBytes.Length; $i++) {
        $match = $true
        for ($j = 0; $j -lt $oldBytes.Length; $j++) {
            if ($Bytes[$i + $j] -ne $oldBytes[$j]) { $match = $false; break }
        }
        if ($match) {
            [Array]::Copy($newBytes, 0, $Bytes, $i, $newBytes.Length)
            $replacements++
            $i += $oldBytes.Length - 1
        }
    }
    return $replacements
}

function Replace-FixedAsciiString([byte[]]$Bytes, [string]$Old, [string]$New) {
    if ($New.Length -gt $Old.Length) { throw "Replacement '$New' is longer than '$Old'." }
    $oldBytes = [Text.Encoding]::ASCII.GetBytes($Old)
    $newBytes = [Text.Encoding]::ASCII.GetBytes($New.PadRight($Old.Length, [char]0))
    $replacements = 0
    for ($i = 0; $i -le $Bytes.Length - $oldBytes.Length; $i++) {
        $match = $true
        for ($j = 0; $j -lt $oldBytes.Length; $j++) {
            if ($Bytes[$i + $j] -ne $oldBytes[$j]) { $match = $false; break }
        }
        if ($match) {
            [Array]::Copy($newBytes, 0, $Bytes, $i, $newBytes.Length)
            $replacements++
            $i += $oldBytes.Length - 1
        }
    }
    return $replacements
}

$exeBytes = [IO.File]::ReadAllBytes($targetExe)
$nameCount = Replace-FixedUtf16String $exeBytes 'Medieval 2 Total War: Kingdoms' 'Steam & Steel'
$fileCount = Replace-FixedUtf16String $exeBytes 'kingdoms.exe' 'M2EX.exe'
$captionCount = Replace-FixedUtf16String $exeBytes 'Medieval II: Total War' 'Steam & Steel'
$shortCaptionCount = Replace-FixedAsciiString $exeBytes 'Medieval 2' 'S&S'
if ($nameCount -lt 3 -or $fileCount -lt 1 -or $captionCount -lt 1 -or $shortCaptionCount -lt 1) {
    throw "Unexpected metadata replacement counts: name=$nameCount filename=$fileCount caption=$captionCount shortcaption=$shortCaptionCount"
}
[IO.File]::WriteAllBytes($targetExe, $exeBytes)

Write-Host "Updated the mod-local $targetExe with the Steam & Steel icon."
