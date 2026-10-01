[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]*$')]
    [string]$Version,

    [string]$OutputRoot,

    [string]$PatchDirectory,

    [switch]$CreateArchive,

    [switch]$AuditDuplicates
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceRoot = (Resolve-Path (Join-Path $scriptDir '..\..')).Path
$rulesPath = Join-Path $scriptDir 'release-allowlist.json'
$rules = Get-Content -LiteralPath $rulesPath -Raw | ConvertFrom-Json
$m2exSync = Join-Path $scriptDir 'Sync-M2EXRuntime.ps1'
& $m2exSync
$installerAssets = @(
    @{ source = 'runtime\prerequisites\vc_redist.x64.exe'; destination = 'payload\prerequisites\vc_redist.x64.exe' }
)

foreach ($asset in $installerAssets) {
    $assetSource = Join-Path $scriptDir $asset.source
    if (-not (Test-Path -LiteralPath $assetSource -PathType Leaf)) {
        throw "Required installer runtime asset is missing: $($asset.source)"
    }
}

$m2exRuntimeRoot = Join-Path $scriptDir 'runtime\m2ex_root'
if (-not (Test-Path -LiteralPath $m2exRuntimeRoot -PathType Container)) {
    throw 'The complete M2EX runtime staging directory was not created.'
}
$requiredM2exRuntime = @(
    'M2EX.exe', 'M2EX.xdb', 'steam_api64.dll', 'mss64.dll', 'binkw64.dll',
    'granny2_x64.dll', 'steam_appid.txt', 'data\descr_difficulty.txt',
    'data\descr_campaign_ai_db_ex.xml'
)
foreach ($relative in $requiredM2exRuntime) {
    if (-not (Test-Path -LiteralPath (Join-Path $m2exRuntimeRoot $relative) -PathType Leaf)) {
        throw "Required M2EX runtime file is missing after synchronization: $relative"
    }
}

if (-not $OutputRoot) {
    $OutputRoot = Join-Path (Split-Path -Parent $sourceRoot) 'steamsteel-release-builds'
}
$outputRootFull = [IO.Path]::GetFullPath($OutputRoot)
$sourceRootFull = [IO.Path]::GetFullPath($sourceRoot)
if ($outputRootFull.TrimEnd('\') -eq $sourceRootFull.TrimEnd('\') -or
    $outputRootFull.StartsWith($sourceRootFull.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'OutputRoot must be outside the Steam & Steel working tree.'
}

$releaseName = "Steam_and_Steel_$Version"
$packageRoot = Join-Path $outputRootFull $releaseName
$stageRoot = Join-Path $packageRoot 'payload\steamsteel'
$manifestRoot = Join-Path $outputRootFull "$releaseName-manifests"

foreach ($required in @($rules.requiredFiles) + @($rules.requiredDirectories)) {
    if (-not (Test-Path -LiteralPath (Join-Path $sourceRootFull $required))) {
        throw "Required release item is missing: $required"
    }
}

if (Test-Path -LiteralPath $packageRoot) {
    $resolvedPackage = [IO.Path]::GetFullPath($packageRoot)
    if (-not $resolvedPackage.StartsWith($outputRootFull.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clear unsafe package path: $resolvedPackage"
    }
    Remove-Item -LiteralPath $resolvedPackage -Recurse -Force
}
New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
New-Item -ItemType Directory -Path $manifestRoot -Force | Out-Null

function Convert-ToRelativePath([string]$FullPath) {
    return [IO.Path]::GetRelativePath($sourceRootFull, $FullPath).Replace('\', '/')
}

$excludedPathSet = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($path in $rules.excludedPaths) {
    [void]$excludedPathSet.Add($path.TrimEnd('/').Replace('\', '/'))
}
$excludedNameSet = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($name in $rules.excludedFileNames) { [void]$excludedNameSet.Add($name) }
$excludedExtensionSet = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($extension in $rules.excludedExtensions) { [void]$excludedExtensionSet.Add($extension) }

function Test-IsExcluded([IO.FileInfo]$File) {
    $relative = Convert-ToRelativePath $File.FullName
    foreach ($excludedPath in $excludedPathSet) {
        if ($relative -eq $excludedPath -or $relative.StartsWith($excludedPath + '/', [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    if ($excludedNameSet.Contains($File.Name)) { return $true }
    if ($excludedExtensionSet.Contains($File.Extension)) { return $true }
    foreach ($suffix in $rules.excludedNameSuffixes) {
        if ($File.Name.EndsWith($suffix, [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

function Test-PathIsExplicitlyExcluded([string]$RelativePath) {
    $normalized = $RelativePath.TrimEnd('/').Replace('\', '/')
    foreach ($excludedPath in $excludedPathSet) {
        if ($normalized -eq $excludedPath -or $normalized.StartsWith($excludedPath + '/', [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

$suspiciousDirectorySet = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($name in $rules.failOnUnlistedDirectoryNames) { [void]$suspiciousDirectorySet.Add($name) }
foreach ($relativeDirectory in $rules.requiredDirectories) {
    $fullDirectory = Join-Path $sourceRootFull $relativeDirectory
    foreach ($directory in Get-ChildItem -LiteralPath $fullDirectory -Directory -Recurse) {
        $relative = Convert-ToRelativePath $directory.FullName
        if ($suspiciousDirectorySet.Contains($directory.Name) -and -not (Test-PathIsExplicitlyExcluded $relative)) {
            throw "Suspicious development directory is inside an allowed runtime root but is not explicitly excluded: $relative"
        }
    }
}

$sourceFiles = [Collections.Generic.List[IO.FileInfo]]::new()
foreach ($relativeFile in @($rules.requiredFiles) + @($rules.optionalFiles)) {
    $fullPath = Join-Path $sourceRootFull $relativeFile
    if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
        $sourceFiles.Add((Get-Item -LiteralPath $fullPath))
    }
}
foreach ($relativeDirectory in $rules.requiredDirectories) {
    $fullDirectory = Join-Path $sourceRootFull $relativeDirectory
    foreach ($file in Get-ChildItem -LiteralPath $fullDirectory -File -Recurse) {
        if (-not (Test-IsExcluded $file)) { $sourceFiles.Add($file) }
    }
}

$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$records = [Collections.Generic.List[object]]::new()
foreach ($file in $sourceFiles) {
    $relative = Convert-ToRelativePath $file.FullName
    if (-not $seen.Add($relative)) { throw "Allowlist selected the same path twice: $relative" }
    $destination = Join-Path $stageRoot $relative.Replace('/', '\')
    $destinationDirectory = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $destination -Force
    $hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
    $records.Add([pscustomobject]@{
        path = $relative
        bytes = $file.Length
        sha256 = $hash
    })
}

foreach ($forbiddenRoot in $rules.forbiddenReleaseRoots) {
    if (Test-Path -LiteralPath (Join-Path $stageRoot $forbiddenRoot)) {
        throw "Forbidden development root entered release staging: $forbiddenRoot"
    }
}

if ($PatchDirectory) {
    $patchRootFull = [IO.Path]::GetFullPath($PatchDirectory)
    if (-not (Test-Path -LiteralPath $patchRootFull -PathType Container)) {
        throw "PatchDirectory does not exist: $patchRootFull"
    }
    foreach ($patchFile in Get-ChildItem -LiteralPath $patchRootFull -File -Recurse) {
        $patchRelative = [IO.Path]::GetRelativePath($patchRootFull, $patchFile.FullName)
        $patchDestination = Join-Path $stageRoot $patchRelative
        New-Item -ItemType Directory -Path (Split-Path -Parent $patchDestination) -Force | Out-Null
        Copy-Item -LiteralPath $patchFile.FullName -Destination $patchDestination -Force
    }
    $records = [Collections.Generic.List[object]]::new()
    foreach ($installedFile in Get-ChildItem -LiteralPath $stageRoot -File -Recurse) {
        $relative = [IO.Path]::GetRelativePath($stageRoot, $installedFile.FullName).Replace('\', '/')
        $records.Add([pscustomobject]@{
            path = $relative
            bytes = $installedFile.Length
            sha256 = (Get-FileHash -LiteralPath $installedFile.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        })
    }
}

$installerAssetRecords = [Collections.Generic.List[object]]::new()
foreach ($asset in $installerAssets) {
    $assetSource = Join-Path $scriptDir $asset.source
    $assetDestination = Join-Path $packageRoot $asset.destination
    New-Item -ItemType Directory -Path (Split-Path -Parent $assetDestination) -Force | Out-Null
    Copy-Item -LiteralPath $assetSource -Destination $assetDestination -Force
    $installedAsset = Get-Item -LiteralPath $assetDestination
    $installerAssetRecords.Add([pscustomobject]@{
        path = $asset.destination.Replace('\', '/')
        bytes = $installedAsset.Length
        sha256 = (Get-FileHash -LiteralPath $installedAsset.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    })
}

foreach ($runtimeFile in Get-ChildItem -LiteralPath $m2exRuntimeRoot -File -Recurse) {
    $relative = [IO.Path]::GetRelativePath($m2exRuntimeRoot, $runtimeFile.FullName)
    $assetDestination = Join-Path $packageRoot (Join-Path 'payload\m2ex_root' $relative)
    New-Item -ItemType Directory -Path (Split-Path -Parent $assetDestination) -Force | Out-Null
    Copy-Item -LiteralPath $runtimeFile.FullName -Destination $assetDestination -Force
    $installerAssetRecords.Add([pscustomobject]@{
        path = ('payload/m2ex_root/' + $relative.Replace('\', '/'))
        bytes = $runtimeFile.Length
        sha256 = (Get-FileHash -LiteralPath $assetDestination -Algorithm SHA256).Hash.ToLowerInvariant()
    })
}

$records = @($records | Sort-Object path)
$totalBytes = ($records | Measure-Object bytes -Sum).Sum
$buildMetadata = [ordered]@{
    schemaVersion = 1
    release = $releaseName
    builtUtc = [DateTime]::UtcNow.ToString('o')
    sourceGitCommit = (& git -C $sourceRootFull rev-parse HEAD).Trim()
    sourceGitDirty = [bool]((& git -C $sourceRootFull status --porcelain).Count)
    fileCount = $records.Count
    totalBytes = $totalBytes
    allowlistSha256 = (Get-FileHash -LiteralPath $rulesPath -Algorithm SHA256).Hash.ToLowerInvariant()
    patchDirectory = if ($PatchDirectory) { [IO.Path]::GetFullPath($PatchDirectory) } else { $null }
    files = $records
    installerAssets = @($installerAssetRecords | Sort-Object path)
}
$manifestJson = Join-Path $manifestRoot 'release-manifest.json'
$buildMetadata | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestJson -Encoding utf8
$records | Export-Csv -LiteralPath (Join-Path $manifestRoot 'release-files.csv') -NoTypeInformation -Encoding utf8

if ($AuditDuplicates) {
    $duplicateGroups = $records | Group-Object sha256 | Where-Object Count -gt 1 | ForEach-Object {
        [pscustomobject]@{
            sha256 = $_.Name
            bytesEach = $_.Group[0].bytes
            copies = $_.Count
            paths = @($_.Group.path)
        }
    }
    $duplicateGroups | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $manifestRoot 'duplicate-content-report.json') -Encoding utf8
}

$installerSource = Join-Path $scriptDir 'SteamAndSteel.iss'
$installerBuildScript = Join-Path $packageRoot 'SteamAndSteel.iss'
Copy-Item -LiteralPath $installerSource -Destination $installerBuildScript -Force
$isccCandidates = @(
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
)
$iscc = $isccCandidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if ($iscc) {
    & $iscc "/DMyAppVersion=$Version" $installerBuildScript
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed with exit code $LASTEXITCODE" }
    Remove-Item -LiteralPath $installerBuildScript -Force
} else {
    Write-Warning 'Inno Setup 6 was not found. Staging is complete, but Setup.exe was not compiled.'
}

if ($CreateArchive) {
    $sevenZipCandidates = @(
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
    )
    $sevenZip = $sevenZipCandidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
    if (-not $sevenZip) {
        $command = Get-Command 7z.exe -ErrorAction SilentlyContinue
        if ($command) { $sevenZip = $command.Source }
    }
    if (-not $sevenZip) { throw '7-Zip was not found. Install it or build staging without -CreateArchive.' }
    $archivePath = Join-Path $outputRootFull "$releaseName.7z"
    if (Test-Path -LiteralPath $archivePath) { Remove-Item -LiteralPath $archivePath -Force }
    # Use 7-Zip's maintained Ultra preset rather than an oversized custom
    # dictionary. -mx=9 is the supported maximum-compression setting; the
    # previous 1536 MiB dictionary made same-day release builds impractically
    # slow while consuming more than 12 GiB of memory.
    # Four compression threads prevent 7-Zip's automatic high-core setting
    # from consuming enough memory/pagefile space to exhaust the release disk.
    & $sevenZip a -t7z -mx=9 -m0=lzma2 -ms=on -mmt=4 $archivePath (Join-Path $packageRoot '*')
    if ($LASTEXITCODE -ne 0) { throw "7-Zip failed with exit code $LASTEXITCODE" }
    & $sevenZip t $archivePath
    if ($LASTEXITCODE -ne 0) { throw "7-Zip archive test failed with exit code $LASTEXITCODE" }
    $archiveHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    "$archiveHash  $([IO.Path]::GetFileName($archivePath))" | Set-Content -LiteralPath (Join-Path $manifestRoot 'SHA256SUMS.txt') -Encoding ascii
}

Write-Host "Release package complete: $packageRoot"
Write-Host "Files: $($records.Count)"
Write-Host "Uncompressed bytes: $totalBytes"
Write-Host "Manifest: $manifestJson"
if ($buildMetadata.sourceGitDirty) {
    Write-Warning 'The source working tree is dirty. This is acceptable for a prerelease test, but the manifest records that fact.'
}
