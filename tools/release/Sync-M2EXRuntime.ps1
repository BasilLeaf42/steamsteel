[CmdletBinding()]
param(
    [string]$GameRoot,
    [string]$ReferenceArchive,
    [string]$Destination,
    [switch]$ArchiveOnly
)

$ErrorActionPreference = 'Stop'

function Get-RelativePathCompat([string]$BasePath, [string]$TargetPath) {
    $baseFull = [IO.Path]::GetFullPath($BasePath).TrimEnd('\') + '\'
    $targetFull = [IO.Path]::GetFullPath($TargetPath)
    if (-not $targetFull.StartsWith($baseFull, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is outside the expected root: $targetFull"
    }
    return $targetFull.Substring($baseFull.Length)
}

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

# Never combine an updated executable from the installed game with the file
# layout of an older distribution.  M2EX adds runtime data, UI and scripts
# between builds; mixing them can leave a package that starts successfully but
# crashes in battle or silently lacks features such as dismounting.
if (-not $ArchiveOnly) {
    $installedM2ex = Join-Path $GameRoot 'M2EX.exe'
    if (-not (Test-Path -LiteralPath $installedM2ex -PathType Leaf)) {
        throw "Installed M2EX executable not found: $installedM2ex"
    }
    $archiveCheckRoot = Join-Path ([IO.Path]::GetTempPath()) ("steamsteel-m2ex-check-" + [guid]::NewGuid().ToString('N'))
    try {
        New-Item -ItemType Directory -Path $archiveCheckRoot -Force | Out-Null
        & $sevenZip e -y "-o$archiveCheckRoot" $ReferenceArchive 'M2EX.exe' | Out-Null
        $archiveM2ex = Join-Path $archiveCheckRoot 'M2EX.exe'
        if (-not (Test-Path -LiteralPath $archiveM2ex -PathType Leaf)) {
            throw "M2EX.exe is missing from reference archive: $ReferenceArchive"
        }
        $installedHash = (Get-FileHash -LiteralPath $installedM2ex -Algorithm SHA256).Hash
        $archiveHash = (Get-FileHash -LiteralPath $archiveM2ex -Algorithm SHA256).Hash
        if ($installedHash -ne $archiveHash) {
            throw "M2EX distribution mismatch: installed executable and reference archive are from different builds."
        }
    } finally {
        if (Test-Path -LiteralPath $archiveCheckRoot) { Remove-Item -LiteralPath $archiveCheckRoot -Recurse -Force }
    }
}

$listing = & $sevenZip l -slt $ReferenceArchive
$paths = foreach ($block in (($listing -join "`n") -split "(?:`r?`n){2,}")) {
    if ($block -notmatch '(?m)^Path = (.+)$') { continue }
    $path = $Matches[1].Trim().Replace('/', '\')
    if ((Split-Path -Leaf $path) -eq (Split-Path -Leaf $ReferenceArchive)) { continue }
    # 7-Zip 25 used `Folder = -` for files. Version 26 emits only an
    # `Attributes` field, with `D` identifying directories.
    if ($block -match '(?m)^Folder = (.+)$' -and $Matches[1].Trim() -ne '-') { continue }
    if ($block -match '(?m)^Attributes = (.+)$' -and $Matches[1].Trim() -match 'D') { continue }
    if ($path -match '^(mods|tools)\\') { continue }
    if ($path -in @('Americas.bat', 'Britannia.bat', 'Crusades.bat', 'Teutonic.bat')) { continue }
    if ($path -match '\.(pdb|lib|exp)$') { continue }
    if ($path -match '^(data|packs|miles|script)\\' -or $path -notmatch '\\') { $path }
}
$paths = @($paths | Sort-Object -Unique)

# Steam & Steel deliberately carries this mod-specific graphics configuration
# even when a particular upstream M2EX test archive omits the file.
$preservedPaths = @('data\graphics\graphics_config.xml')
foreach ($preservedPath in $preservedPaths) {
    if (Test-Path -LiteralPath (Join-Path $GameRoot $preservedPath) -PathType Leaf) {
        $paths += $preservedPath
    }
}
$paths = @($paths | Sort-Object -Unique)
if ($paths.Count -lt 100) { throw "M2EX runtime selection is unexpectedly small ($($paths.Count) files)." }

$destinationFull = [IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationFull) { Remove-Item -LiteralPath $destinationFull -Recurse -Force }
New-Item -ItemType Directory -Path $destinationFull -Force | Out-Null

$fallbackRoot = Join-Path ([IO.Path]::GetTempPath()) ("steamsteel-m2ex-" + [guid]::NewGuid().ToString('N'))
try {
    if ($ArchiveOnly) {
        New-Item -ItemType Directory -Path $fallbackRoot -Force | Out-Null
        & $sevenZip x -y "-o$fallbackRoot" $ReferenceArchive | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Failed to extract M2EX distribution: $ReferenceArchive" }
    }
    foreach ($relative in $paths) {
        $source = if ($ArchiveOnly -and $relative -notin $preservedPaths) { Join-Path $fallbackRoot $relative } else { Join-Path $GameRoot $relative }
        if ($source -and (Test-Path -LiteralPath $source -PathType Container)) { continue }
        if (-not $source -or -not (Test-Path -LiteralPath $source -PathType Leaf)) {
            if ($ArchiveOnly) { throw "M2EX runtime file unavailable after archive extraction: $relative" }
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

# The public executable is renamed for branding. Keep a matching symbol file
# name so M2EX crash reports resolve engine frames instead of reporting that
# the XDB was not loaded.
$m2exSymbols = Join-Path $destinationFull 'M2EX.xdb'
if (Test-Path -LiteralPath $m2exSymbols -PathType Leaf) {
    Copy-Item -LiteralPath $m2exSymbols -Destination (Join-Path $destinationFull 'SteamAndSteel.xdb') -Force
}

$manifest = foreach ($file in Get-ChildItem -LiteralPath $destinationFull -File -Recurse) {
    [pscustomobject]@{
        path = (Get-RelativePathCompat $destinationFull $file.FullName).Replace('\', '/')
        bytes = $file.Length
        sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$manifest | Sort-Object path | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $scriptDir 'm2ex-runtime-manifest.json') -Encoding utf8
$sourceDescription = if ($ArchiveOnly) { 'the verified distribution archive' } else { 'the current installed game root' }
Write-Host "Staged $($manifest.Count) M2EX runtime files from $sourceDescription using $ReferenceArchive."
