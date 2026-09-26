$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$archive = Join-Path $PSScriptRoot 'medieval_portrait_removal_20260925\originals'

foreach ($culture in @('northern_european', 'southern_european', 'slavic', 'chinese', 'mesoamerican')) {
    foreach ($age in @('young', 'old')) {
        $source = Join-Path $archive "$culture\$age\rogues"
        if (-not (Test-Path -LiteralPath $source)) {
            continue
        }
        $destination = Join-Path $root "data\ui\$culture\portraits\portraits\$age\rogues"
        Get-ChildItem -LiteralPath $destination -File | Remove-Item
        Get-ChildItem -LiteralPath $source -File | Copy-Item -Destination $destination
    }
}

Write-Output 'Restored all affected assassin/spy portrait pools from archive.'
