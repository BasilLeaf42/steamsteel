$ErrorActionPreference = 'Stop'

$paths = @('data/export_descr_unit.txt', 'data/tow_steamsteel/export_descr_unit.txt')
$excludedPattern = '(?i)(maxim|gatling|mitraill|machine|pompom|pom.?pom|nordenfelt|hotchkiss)'

foreach ($path in $paths) {
    $text = [IO.File]::ReadAllText((Resolve-Path $path)).Replace("`r`n", "`n").Replace("`r", "`n")
    $newline = "`n"
    $blocks = [regex]::Split($text, '(?m)(?=^type\s+)')
    $changed = 0

    for ($i = 0; $i -lt $blocks.Count; $i++) {
        $block = $blocks[$i]
        if ($block -notmatch '(?m)^category\s+siege\s*$') { continue }

        $type = ([regex]::Match($block, '(?m)^type\s+(.+)$')).Groups[1].Value.Trim()
        $engine = ([regex]::Match($block, '(?m)^engine\s+(.+)$')).Groups[1].Value.Trim()
        $dictionary = ([regex]::Match($block, '(?m)^dictionary\s+(.+)$')).Groups[1].Value.Trim()
        if ("$type $engine $dictionary" -match $excludedPattern) { continue }

        if ($block -notmatch '(?m)^attributes\s+.*(?:^|,\s*)artillery(?:\s*,|$)') {
            throw "Conventional artillery lacks the artillery attribute: $type"
        }

        $block = [regex]::Replace($block, '(?m)^(attributes\s+.+?),\s*no_custom\s*$', '$1')
        $ownershipMatch = [regex]::Match($block, '(?m)^ownership\s+(.+)$')
        if (-not $ownershipMatch.Success) { throw "Missing ownership line: $type" }

        $owners = @($ownershipMatch.Groups[1].Value.Split(',') | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        if ($type -eq 'col_12lb') {
            foreach ($faction in @('egypt', 'timurids', 'lith')) {
                if ($faction -notin $owners) { $owners += $faction }
            }
            $block = [regex]::Replace($block, '(?m)^ownership\s+.+$', 'ownership        ' + ($owners -join ', '))
        }

        $customOwners = @($owners | Where-Object { $_ -ne 'slave' })
        $block = [regex]::Replace($block, '(?m)^era [012]\s+.*\r?\n', '')
        if ($customOwners.Count -gt 0) {
            $eraLines = "era 0            $($customOwners -join ', ')${newline}era 1            $($customOwners -join ', ')${newline}era 2            $($customOwners -join ', ')"
            $block = [regex]::Replace($block, '(?m)^(ownership\s+.+)$', "`$1${newline}$eraLines")
        }

        if ($block -ne $blocks[$i]) { $blocks[$i] = $block; $changed++ }
    }

    [IO.File]::WriteAllText((Resolve-Path $path), ($blocks -join ''), [Text.UTF8Encoding]::new($false))
    Write-Host "$path : normalized $changed conventional artillery records"
}
