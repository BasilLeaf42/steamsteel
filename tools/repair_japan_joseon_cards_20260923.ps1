$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$cards = Join-Path $root 'data\ui\units\saxons'
$backup = Join-Path $root 'tools\card_source_archive\japan_before_general_zoom_joseon_repair_20260923'
New-Item -ItemType Directory -Force -Path $backup | Out-Null

$faces = @(
  'Japan_Bodyguard_Retainers','Japan_Enomoto_Takeaki','Japan_Hijikata_Toshizo',
  'Japan_Itagaki_Taisuke','Japan_Jules_Brunet','Japan_Kondo_Isami',
  'Japan_Matsudaira_Katamori','Japan_Saigo_Takamori_1860','Japan_Sakamoto_Ryoma',
  'Japan_Takeda_Ayasaburo','Japan_Tokugawa_Yoshinobu'
)
$lessZoomed = Join-Path $root 'tools\card_source_archive\japan_before_second_close_crop_20260919'
foreach ($key in $faces) {
  $name = "#$key.tga"
  Copy-Item -LiteralPath (Join-Path $cards $name) -Destination (Join-Path $backup $name) -Force
  Copy-Item -LiteralPath (Join-Path $lessZoomed $name) -Destination (Join-Path $cards $name) -Force
}

$ryukihei = '#Japan_Ryukihei_1870.tga'
$preNormalization = Join-Path $root 'tools\card_source_archive\all_cards_before_systemic_background_20260923\saxons'
Copy-Item -LiteralPath (Join-Path $cards $ryukihei) -Destination (Join-Path $backup $ryukihei) -Force
Copy-Item -LiteralPath (Join-Path $preNormalization $ryukihei) -Destination (Join-Path $cards $ryukihei) -Force

$mercs = Join-Path $root 'data\ui\units\mercs'
foreach ($key in @('korean_archers','Korean_Byeolgigun','Korean_Gimagungsu','Korean_Musketeers','Korean_Pikemen','korean_rifles_mercs','korean_cav_mercs')) {
  $name = "#$key.tga"
  $target = Join-Path $mercs $name
  if (Test-Path -LiteralPath $target) { Copy-Item -LiteralPath $target -Destination (Join-Path $backup "mercs_$name") -Force }
  Copy-Item -LiteralPath (Join-Path $cards $name) -Destination $target -Force
}

Write-Output "Restored $($faces.Count) less-cropped Japanese command portraits, repaired Teikoku Ryukihei 1870, and installed 7 Joseon mercenary cards."
