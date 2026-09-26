# Steam & Steel campaign portrait and event-art audit — 2026-09-25

No artwork was replaced during this audit.

## Campaign portrait pools

The seven active portrait mappings contain 5,994 physical TGA files, including 1,526 general portraits. File duplication reduces the general pool to 809 distinct images.

| Portrait mapping | All files | General files | Distinct general images |
|---|---:|---:|---:|
| southern_european | 712 | 278 | 138 |
| northern_european | 1,082 | 232 | 116 |
| mesoamerican | 1,339 | 204 | 50 |
| slavic | 395 | 138 | 69 |
| middle_eastern | 694 | 248 | 124 |
| asian | 525 | 202 | 100 |
| chinese | 1,247 | 224 | 112 |

Every one of the 763 same-number young/old general pairs is byte-identical. The pools therefore provide no visual ageing. Visual review also shows that the replacement sets are highly uniform synthetic portrait series rather than faction-specific pools. Their cultures are especially broad:

- `southern_european` is shared by Spain, France, Brazil, Austria-Hungary, Mexico, the Boers, Greece, Italy, Argentina and Peru.
- `northern_european` is shared by Prussia, Sweden-Norway, Denmark, the Netherlands, the Union, the Confederacy and Britain.
- `asian` is shared by Qajar Persia, Turkestan, Afghanistan and the Indian Princely States.
- `chinese` is shared by Siam, Qing and Japan.
- `mesoamerican` is repurposed for Zulu and Ethiopia.

The sets are period-looking but generic, and cannot reliably distinguish national uniform, class, service, or faction. The age duplication makes them unsuitable as a finished campaign portrait system.

## Named campaign portraits

- 36 active portrait references resolve to 34 distinct named portrait directories.
- All referenced directory names exist.
- Six referenced portraits have incomplete age/death sets:
  - `abdulmejid`: no young portrait
  - `binsaid`: no dead portrait
  - `davis`: no young portrait
  - `dostmuhamedkhan`: no young portrait
  - `juarez`: no young portrait
  - `lincoln`: no young portrait
- Of all 63 named portrait directories, only 53 contain all three files.
- Twenty-five complete sets use exactly the same image for young, old and dead.
- Forty-two named sets use the same image for young and old; only twelve have distinct ageing art.

Most named portraits are genuine photographs, engravings, or painted portraits and should be preserved. Several campaign assignments are visibly generic or identity-mismatched and require a separate identity audit, notably `india` for Sher Ali, `mohammed` for the Moroccan ruler, `shaka` for Cetshwayo, and generic `kokand`/`qing_emp` portraits.

## Event screens

There are 103 event-picture filenames but 114 distinct image hashes because some same-named files differ between cultures.

Thirty filenames are untouched or directly recycled Medieval II-era subjects: the Black Death series, earthquake series, medieval inventions, medieval science screens, Mongol/Timurid warnings, football ban, gunpowder discovery, Grote Mandrenke and world-is-round art. Many are exact duplicates under different event names:

- all five earthquake filenames share the same image;
- eleven invention filenames share one image within a culture;
- the science events reuse the same book image;
- Mongol and Timurid warnings share one image;
- most Black Death stages reuse the same image.

The new material is inconsistent. Faction introductions alternate between bare modern flags and generic synthetic scenes. Military-reform and technology screens are mostly generic generated or stock-like compositions rather than documented event-specific art.

### Missing scripted event art

These active scripted events have no matching TGA in any culture:

- `byzantine_restoration`
- `incan_empire`
- `ishin_chosen`
- `ishin_decision`
- `ishin_satcho`
- `roman_empire_restored`
- `shogun_chosen`
- `timurid_unified`

### Faction introductions installed under the wrong culture

- Austria-Hungary uses `southern_european`, but `AH_EVENT.tga` is absent there.
- Qajar Persia uses `asian`, but `QAJARI_EVENT.tga` is absent there.
- Japan uses `chinese`, but both `SHOGUN_EVENT.tga` and `MEIJI_EVENT.tga` are absent there.

Other faction announcements generally have at least one correctly placed copy, although many unnecessary copies exist under unrelated cultures.

## Recommended repair order

1. Add the eight entirely missing scripted event screens and correct the four faction-introduction placements.
2. Replace the thirty medieval event remnants, beginning with events that actually occur in the Steam & Steel date range.
3. Replace flag-only faction introductions with sourced portraits, state ceremonies, capitals, armies, or contemporary national scenes.
4. Preserve genuine named historical portraits, repair the six incomplete sets, and correct identity mismatches.
5. Replace the generic general pools faction by faction. At minimum, create distinct young and old pools; do not merely duplicate the same portrait into both folders.
6. Audit agents after generals, because the general pools are the most visible and the existing culture mappings conflate several unrelated factions.

Visual review sheets:

- `tools/campaign_general_portrait_pool_contact_sheet_20260925.jpg`
- `tools/named_campaign_portraits_contact_sheet_20260925.jpg`
- `tools/event_screen_contact_sheet_20260925.jpg`
