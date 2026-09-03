param(
    [switch]$Apply
)

# Primary missile damage is round(projectile calibre in mm ^ 1.25).
# The explicit cases are projectile/bore calibres; only the last four cases are
# intentionally generic defaults for weapons which are not named in the EDU.
function Get-DamageTarget([string]$description, [string]$projectile) {
    $d = $description.ToLowerInvariant()
    $mm = $null

    # Named arms and cartridges.  Keep specific variants before family names.
    if ($d -match 'pistol|revolver') { return 20 }
    elseif ($d -match 'fusil (?:español )?rayado modelo 1859|carabina rayada modelo 1857') { $mm = 14.8 }
    elseif ($d -match 'martini.{0,3}henry|peabody-martini') { $mm = 11.43 }
    elseif ($d -match 'snider|pattern 1853 enfield|p53 enfield|enfield pattern 1853|wilson-enfield|pattern 1858 enfield|pattern 1859 enfield|espingarda enfield.*m/1859') { $mm = 14.7 }
    elseif ($d -match 'brown bess') { $mm = 19.05 }
    elseif ($d -match 'baker') { $mm = 15.88 }
    elseif ($d -match 'whitworth') { $mm = 11.46 }
    elseif ($d -match 'chassepot|\bgras\b') { $mm = 11.0 }
    elseif ($d -match 'tabati.re') { $mm = 14.7 }
    elseif ($d -match 'remington rolling block swedish') { $mm = 12.17 }
    elseif ($d -match 'remington rolling block|remington m1868|remington modelo 1868|tercerola remington|no\. 1 remington') { $mm = 12.7 }
    elseif ($d -match 'mauser m1871|mauser model 1871') { $mm = 11.15 }
    elseif ($d -match 'mauser m1890|mauser model 1895|mauser modelo 1895|mauser modelo 1891|mauser m1893|fusil mauser|carabina mauser|tercerola mauser') { $mm = 7.65 }
    elseif ($d -match 'lebel') { $mm = 8.0 }
    elseif ($d -match 'lee.{0,3}metford|lee.{0,3}enfield') { $mm = 7.7 }
    elseif ($d -match 'gewehr m1888|gewehr m1898|hanyang 88|mosin') { $mm = 7.92 }
    elseif ($d -match 'carcano') { $mm = 6.5 }
    elseif ($d -match 'krag-j.rgensen m1889') { $mm = 8.0 }
    elseif ($d -match 'krag-j.rgensen|m1898 krag') { $mm = 7.62 }
    elseif ($d -match 'mannlicher m1895|mannlicher m1888') { $mm = 8.0 }
    elseif ($d -match 'mannlicher model 1886') { $mm = 11.0 }
    elseif ($d -match 'vetterli') { $mm = 10.4 }
    elseif ($d -match 'beaumont') { $mm = 11.3 }
    elseif ($d -match 'berdan') { $mm = 10.67 }
    elseif ($d -match 'dreyse|z.ndnadel') { $mm = 15.43 }
    elseif ($d -match 'werder') { $mm = 11.5 }
    elseif ($d -match 'w.nz(l|l)') { $mm = 14.0 }
    elseif ($d -match 'mylonas') { $mm = 11.15 }
    elseif ($d -match 'westley.?richards') { $mm = 11.43 }
    elseif ($d -match 'joslyn') { $mm = 14.22 }
    elseif ($d -match 'henry rifle|winchester model 1866') { $mm = 11.18 }
    elseif ($d -match 'spencer') { $mm = 14.22 }
    elseif ($d -match 'burnside|starr') { $mm = 13.72 }
    elseif ($d -match 'sharps|maynard') { $mm = 13.21 }
    elseif ($d -match 'springfield model 1873|springfield model 1884') { $mm = 11.63 }
    elseif ($d -match 'springfield|mississippi') { $mm = 14.73 }
    elseif ($d -match 'lorenz') { $mm = 13.9 }
    elseif ($d -match 'fucile di fanteria modello 1860|fusil min|m1842 chatellerault|pattern 1851 minie|m-1854|m-1856|m-1844|wrede|kammerlader|tapriffel|ktoros') { $mm = 17.8 }
    elseif ($d -match 'm-1857 six line') { $mm = 15.24 }
    elseif ($d -match 'african trade musket|trade musket|matchlock|moukhala|\bmusket\b|smoothbore') { $mm = 17.8 }
    elseif ($d -match 'arquebus|harquebus') { $mm = 16.0 }
    # Unnamed weapons: typical historical bore diameters, per request.
    elseif ($projectile -match 'arquebus|harquebus') { $mm = 16.0 }
    elseif ($projectile -match 'rifled_musket') { $mm = 14.7 }
    elseif ($projectile -match '^musket') { $mm = 17.8 }
    elseif ($projectile -match 'magazine_rifle|rifle_carbine') { $mm = 7.7 }
    elseif ($projectile -match '^rifle') { $mm = 11.0 }

    if ($null -eq $mm) { return $null }
    return [math]::Round([math]::Pow($mm, 1.25), 0, [MidpointRounding]::AwayFromZero)
}

$edu = Join-Path $PSScriptRoot '..\data\tow_steamsteel\export_descr_unit.txt'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$lines = [System.Collections.Generic.List[string]]([System.IO.File]::ReadAllLines($edu, $utf8NoBom))
$type = ''; $description = ''; $changes = @(); $unresolved = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^type\s+(\S+)') { $type = $Matches[1]; $description = ''; continue }
    if ($lines[$i] -match '^dictionary\s+\S+\s*;\s*(.*)$') { $description = $Matches[1]; continue }
    if ($lines[$i] -notmatch '^(stat_pri\s+)(\d+)(\s*,\s*\d+\s*,\s*([^,]+),.*\bmissile\b.*)$') { continue }
    # Regex operations inside Get-DamageTarget overwrite PowerShell's automatic
    # $Matches variable, so retain every capture before calling it.
    $prefix = $Matches[1]; $old = [int]$Matches[2]; $tail = $Matches[3]
    $projectile = $Matches[4].Trim()
    if ($projectile -notmatch '(?:arquebus|harquebus|musket|rifle).*bullet') { continue }
    $target = Get-DamageTarget $description $projectile
    if ($null -eq $target) { $unresolved += "line $($i + 1): $type | $description | $projectile"; continue }
    if ($old -ne $target) {
        $changes += [pscustomobject]@{ Line = $i + 1; Type = $type; Description = $description; Projectile = $projectile; Old = $old; New = $target }
        if ($Apply) { $lines[$i] = $prefix + $target + $tail }
    }
}

if ($Apply) { [System.IO.File]::WriteAllLines($edu, $lines, $utf8NoBom) }
"$($changes.Count) firearm primary-damage changes$(if($Apply){' applied'}else{' proposed'})."
if ($unresolved.Count) { 'UNRESOLVED:'; $unresolved }
$changes | Sort-Object Line | Format-Table -AutoSize
