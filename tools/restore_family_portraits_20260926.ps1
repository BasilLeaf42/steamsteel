$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$archive = Join-Path $PSScriptRoot 'medieval_portrait_removal_20260925\originals'

foreach ($culture in @('northern_european', 'southern_european', 'slavic', 'mesoamerican')) {
    $source = Join-Path $archive "$culture\family"
    $destination = Join-Path $root "data\ui\$culture\portraits\family"
    if (-not (Test-Path -LiteralPath $source)) {
        throw "Missing family backup: $source"
    }
    Get-ChildItem -LiteralPath $source -File | Copy-Item -Destination $destination -Force
}

Write-Output 'Restored all family portrait files from the pre-cleanup archive.'
