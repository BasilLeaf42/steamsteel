$ErrorActionPreference = 'Stop'

$paths = @('data/export_descr_unit.txt', 'data/tow_steamsteel/export_descr_unit.txt')
foreach ($path in $paths) {
    $text = [System.IO.File]::ReadAllText((Resolve-Path $path))
    $blocks = [regex]::Split($text, '(?m)(?=^type\s+)')
    $changed = 0
    for ($i = 0; $i -lt $blocks.Count; $i++) {
        if ($blocks[$i] -notmatch '(?m)^type\s+Japan .+ (?:1890|1900|1905)\s*$') { continue }
        $updated = [regex]::Replace($blocks[$i], '(?m)^era 2\s+saxons,?\s*\r?\n', '')
        if ($updated -ne $blocks[$i]) { $blocks[$i] = $updated; $changed++ }
    }
    [System.IO.File]::WriteAllText((Resolve-Path $path), ($blocks -join ''), [System.Text.UTF8Encoding]::new($false))
    Write-Host "$path : removed late custom-battle membership from $changed records"
}
