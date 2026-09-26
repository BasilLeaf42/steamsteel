$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$archive = Join-Path $PSScriptRoot 'medieval_portrait_removal_20260925\originals'
$cultures = @('northern_european', 'southern_european', 'slavic')

function Backup-Directory([string]$source, [string]$relative) {
    $destination = Join-Path $archive $relative
    if (-not (Test-Path -LiteralPath $destination)) {
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $destination -Recurse
    }
}

foreach ($culture in $cultures) {
    $rogues = Join-Path $root "data\ui\$culture\portraits\portraits\young\rogues"
    Backup-Directory $rogues "$culture\young\rogues"
    foreach ($id in 52..55) {
        $file = Join-Path $rogues ('{0:D3}.tga' -f $id)
        if (Test-Path -LiteralPath $file) {
            Remove-Item -LiteralPath $file
        }
    }
}

foreach ($culture in @('chinese', 'mesoamerican')) {
    foreach ($age in @('young', 'old')) {
        $base = Join-Path $root "data\ui\$culture\portraits\portraits\$age"
        $rogues = Join-Path $base 'rogues'
        $civilians = Join-Path $base 'civilians'
        Backup-Directory $rogues "$culture\$age\rogues"

        Get-ChildItem -LiteralPath $rogues -File | Remove-Item
        foreach ($id in 0..55) {
            $name = '{0:D3}.tga' -f $id
            $source = Join-Path $civilians $name
            if (-not (Test-Path -LiteralPath $source)) {
                throw "Missing verified donor: $source"
            }
            Copy-Item -LiteralPath $source -Destination (Join-Path $rogues $name)
        }
    }
}

# Replace the remaining Western medieval/fantasy family paintings with existing
# nineteenth-century royal portraits. These pools already shared one family set.
foreach ($culture in @('northern_european', 'southern_european', 'slavic')) {
    $family = Join-Path $root "data\ui\$culture\portraits\family"
    Backup-Directory $family "$culture\family"
    Copy-Item -LiteralPath (Join-Path $root 'data\ui\custom_portraits\qeliza\portrait_old.tga') -Destination (Join-Path $family 'wife.tga') -Force
    Copy-Item -LiteralPath (Join-Path $root 'data\ui\custom_portraits\isabella\portrait_old.tga') -Destination (Join-Path $family 'daughter.tga') -Force
}

# Replace the sepia fantasy family set used by the African culture with verified
# portraits already present in that culture's nineteenth-century civilian pool.
$mesoFamily = Join-Path $root 'data\ui\mesoamerican\portraits\family'
Backup-Directory $mesoFamily 'mesoamerican\family'
Copy-Item -LiteralPath (Join-Path $root 'data\ui\mesoamerican\portraits\portraits\young\civilians\000.tga') -Destination (Join-Path $mesoFamily 'wife.tga') -Force
Copy-Item -LiteralPath (Join-Path $root 'data\ui\mesoamerican\portraits\portraits\young\civilians\001.tga') -Destination (Join-Path $mesoFamily 'daughter.tga') -Force
Copy-Item -LiteralPath (Join-Path $root 'data\ui\mesoamerican\portraits\portraits\young\civilians\003.tga') -Destination (Join-Path $mesoFamily 'son.tga') -Force

Write-Output "Removed medieval rogue holdovers; originals archived at $archive"
