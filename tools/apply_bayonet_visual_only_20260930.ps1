$ErrorActionPreference = 'Stop'

# Restore the visually correct pike soldier animation for verified bayonet models.
$modelPath = 'data\unit_models\battle_models.modeldb'
$model = [IO.File]::ReadAllText((Resolve-Path $modelPath), [Text.Encoding]::ASCII)
$modelCount = ([regex]::Matches($model, '13 MTW2_Pike_Old')).Count
if ($modelCount -ne 407) { throw "Expected 407 MTW2_Pike_Old mappings, found $modelCount" }
$model = $model.Replace('13 MTW2_Pike_Old', '9 MTW2_Pike')
[IO.File]::WriteAllText((Resolve-Path $modelPath), $model, [Text.Encoding]::ASCII)

function Update-EduBayonets([string]$path) {
    $raw = [IO.File]::ReadAllText((Resolve-Path $path), [Text.Encoding]::UTF8)
    $script:changed = 0
    $updated = [regex]::Replace($raw, '(?ms)^type\s+.*?(?=^type\s+|\z)', {
        param($match)
        $block = $match.Value
        $isFirearm = $block -match '(?m)^stat_pri\s+[^\r\n]*(arquebus|harquebus|musket|rifle|wall_gun|long_gun|flintlock)[^\r\n]*$'
        $isBayonet = $block -match '(?m)^stat_sec_attr\s+[^\r\n]*short_pike'
        if (-not ($isFirearm -and $isBayonet)) { return $block }

        $block = [regex]::Replace(
            $block,
            '(?m)^(stat_sec\s+[^\r\n]*,\s*)spear(\s*,\s*[^\r\n]*)$',
            '${1}sword${2}'
        )
        $block = [regex]::Replace($block, '(?m)^stat_sec_attr\s+[^\r\n]*$', 'stat_sec_attr    no')
        $script:changed++
        return $block
    })
    [IO.File]::WriteAllText((Resolve-Path $path), $updated, [Text.UTF8Encoding]::new($false))
    return $script:changed
}

$towCount = Update-EduBayonets 'data\tow_steamsteel\export_descr_unit.txt'
$mainCount = Update-EduBayonets 'data\export_descr_unit.txt'
Write-Output "Restored $modelCount model mappings to MTW2_Pike."
Write-Output "Converted verified bayonet combat behaviour to ordinary melee blade: tow=$towCount main=$mainCount."
