[CmdletBinding()]
param(
    [string]$GameRoot,
    [string]$ReferenceArchive,
    [string]$Destination
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $GameRoot) { $GameRoot = (Resolve-Path (Join-Path $scriptDir '..\..\..\..')).Path }
if (-not $ReferenceArchive) { $ReferenceArchive = Join-Path $GameRoot 'M2EX.7z' }
if (-not $Destination) { $Destination = Join-Path $scriptDir 'runtime\m2ex_root' }

$sevenZip = @(
    "$env:ProgramFiles\7-Zip\7z.exe",
    "${env:ProgramFiles(x86)}\7-Zip\7z.exe",
    (Get-Command 7z.exe -ErrorAction SilentlyContinue).Source
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if (-not $sevenZip) { throw '7-Zip is required to read the verified M2EX distribution.' }
if (-not (Test-Path -LiteralPath $ReferenceArchive -PathType Leaf)) { throw "M2EX reference archive not found: $ReferenceArchive" }

$listing = & $sevenZip l -slt $ReferenceArchive
$paths = foreach ($line in $listing) {
    if ($line -notmatch '^Path = (.+)$') { continue }
    $path = $Matches[1].Replace('/', '\')
    if ($path -eq (Split-Path -Leaf $ReferenceArchive)) { continue }
    if ($path.EndsWith('\')) { continue }
    if ($path -match '^(mods|tools)\\') { continue }
    if ($path -in @('Americas.bat', 'Britannia.bat', 'Crusades.bat', 'Teutonic.bat')) { continue }
    if ($path -match '\.(pdb|lib|exp)$') { continue }
    if ($path -match '(^|\\)[^\\]*d_43\.dll$') { continue }
    if ($path -match '^(data|packs|miles)\\' -or $path -notmatch '\\') { $path }
}
$paths = @($paths | Sort-Object -Unique)
if ($paths.Count -lt 100) { throw "M2EX runtime selection is unexpectedly small ($($paths.Count) files)." }

$destinationFull = [IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationFull) { Remove-Item -LiteralPath $destinationFull -Recurse -Force }
New-Item -ItemType Directory -Path $destinationFull -Force | Out-Null

$fallbackRoot = Join-Path ([IO.Path]::GetTempPath()) ("steamsteel-m2ex-" + [guid]::NewGuid().ToString('N'))
try {
    foreach ($relative in $paths) {
        $source = Join-Path $GameRoot $relative
        if (Test-Path -LiteralPath $source -PathType Container) { continue }
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
            New-Item -ItemType Directory -Path $fallbackRoot -Force | Out-Null
            & $sevenZip e -y "-o$fallbackRoot" $ReferenceArchive $relative | Out-Null
            $source = Join-Path $fallbackRoot (Split-Path -Leaf $relative)
        }
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "M2EX runtime file unavailable: $relative" }
        $target = Join-Path $destinationFull $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $target -Force
    }
} finally {
    if (Test-Path -LiteralPath $fallbackRoot) { Remove-Item -LiteralPath $fallbackRoot -Recurse -Force }
}

$manifest = foreach ($file in Get-ChildItem -LiteralPath $destinationFull -File -Recurse) {
    [pscustomobject]@{
        path = [IO.Path]::GetRelativePath($destinationFull, $file.FullName).Replace('\', '/')
        bytes = $file.Length
        sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$manifest | Sort-Object path | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $scriptDir 'm2ex-runtime-manifest.json') -Encoding utf8
Write-Host "Staged $($manifest.Count) M2EX runtime files from the current installed game root."
