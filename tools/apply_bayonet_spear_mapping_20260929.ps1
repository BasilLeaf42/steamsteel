$ErrorActionPreference = 'Stop'
$eduPath = 'data\tow_steamsteel\export_descr_unit.txt'
$modelPath = 'data\unit_models\battle_models.modeldb'

$edu = Get-Content -LiteralPath $eduPath -Raw
$targets = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($block in [regex]::Split($edu, '(?m)(?=^type\s+)')) {
    if ($block -match '(?m)^soldier\s+([^,\r\n]+)') {
        $soldier = $matches[1].Trim()
        $firearm = $block -match '(?m)^stat_pri\s+[^\r\n]*(arquebus|harquebus|musket|rifle|wall_gun|long_gun|flintlock)[^\r\n]*$'
        $bayonet = $block -match '(?m)^stat_sec_attr\s+[^\r\n]*short_pike'
        if ($firearm -and $bayonet) { [void]$targets.Add($soldier) }
    }
}

$raw = [IO.File]::ReadAllText((Resolve-Path $modelPath), [Text.Encoding]::ASCII)
$script:changed = 0
$entryPattern = '(?ms)^\d+ (?<name>[^\s]+)\s*\r?\n\d+ \d+\s*\r?\n.*?(?=^\d+ [^\s]+\s*\r?\n\d+ \d+\s*\r?\n|\z)'
$updated = [regex]::Replace($raw, $entryPattern, {
    param($match)
    if ($targets.Contains($match.Groups['name'].Value) -and $match.Value -match '(^|\s)20 MTW2_Halberd_Primary(\s|$)') {
        $script:changed++
        $entry = [regex]::Replace($match.Value, '(^|\s)20 MTW2_Halberd_Primary(\s|$)', '${1}13 MTW2_Pike_Old${2}')
        return $entry
    }
    return $match.Value
})

if ($script:changed -ne 407) {
    throw "Expected 407 verified bayonet mappings including the pre-existing Japanese halberd-animation precedents, found $script:changed"
}
[IO.File]::WriteAllText((Resolve-Path $modelPath), $updated, [Text.Encoding]::ASCII)
Write-Output "Mapped $script:changed verified bayonet models to MTW2_Pike_Old with MTW2_Pike_primary retained."
