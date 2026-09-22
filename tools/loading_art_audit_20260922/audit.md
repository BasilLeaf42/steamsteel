# Loading-screen artwork audit

**All 62 audited screens are flagged “AI — user flagged” at the user’s request.** Authorship remains unverified; this includes legacy screen 19. The visual-quality findings below remain separate.

Visual audit of installed loading artwork — 22 September 2026

All 62 numbered screens currently in data/loading_screen were visually reviewed in labelled 768-pixel-wide previews. Sixteen selected screens were also inspected individually at the native 1024-pixel artwork width. This is a visual-quality audit, not proof of AI authorship or authentication of historical subjects. No game launch or historical source matching was performed.

Findings: 8 replace; 31 review; 23 retain provisionally. Retain means no comparable major defect was identified at the inspected scale, not a historical or licensing approval. Review distinguishes unresolved details from definite replacement recommendations.

The source set data/loading_screen/load_steamsteel contains 61 numbered images, all byte-identical to their installed counterparts. The load_althis set has the same 61 images. Neither contains screen 19. The installed screen 19 matches load_europe/Loading_screen_19.tga and load_greatgame/Loading_screen_19.tga (also repeated under other slot numbers). Steam & Steel.bat line 9 copies the selected loading folder over the runtime folder without clearing unmatched files. This permits stale screens to survive. Actual engine selection frequency was not tested.

Inventory covers 557 TGA files across the runtime folder and eight source sets: 284 byte-distinct assets, including loading bar/logo. The 220 distinct assets outside the numbered runtime set were inventoried and previewed to files, but were NOT given a complete visual audit. Findings below cover all artwork installed for the supplied Steam & Steel launcher, including its stale slot.

The December 10, 2025 commit 269c210a (Loading Screen Overhaul) changed 372 loading-art files. Its message contains no authorship explanation. Earlier versions survive in its parent; four example slots were extracted into this report folder without modifying game files. Their subjects differ, so restoration requires selection rather than assuming identical slot subjects. Visual anomalies are consistent with poorly controlled generated illustration, but file appearance and the commit title do not establish the generating tool or authorship.

Priority: replace screens 5, 7, 8, 13, 21, 25, 37 and 52. Strongest mechanical/anatomical examples are 5, 8, 25 and 52. Preserve existing artwork; prefer independently sourced period artwork or the recoverable prior collection after attribution and suitability checks. Review vehicle machinery, hands and mounted overlaps next. Any future installation must update source and runtime consistently and explicitly handle stale slots.

No installed art, launcher or gameplay file was changed. PNG/JPEG files here are audit previews only. inventory.json preserves paths and SHA-256 hashes; findings.json records per-screen decisions.


| Screen | Decision | Finding |
|---|---|---|
| 1 | Review | Bridge construction: several workers merge with scaffold members; joints and tool contacts need closer reconstruction. |
| 2 | Retain provisionally | Harbour delegation: coherent principal figures and composition; small troop details are soft. |
| 3 | Review | Polar balloon: suspension ropes, basket attachments and clustered figures are visually confused. |
| 4 | Retain provisionally | Warship: clear silhouette and atmosphere; exact ship identity and rigging remain unverified. |
| 5 | Replace | Firing line: repeated overlapping arms and stocks do not resolve into clean individual rifle grips; right-hand rank dissolves into isolated weapon fragments. |
| 6 | Review | Royal montage: intentionally symbolic composition, but costume and person identification require source documentation. |
| 7 | Replace | Warriors: the kneeling archer has multiple competing bow/arrow lines through his face and grip; the main rifle action and hand contact are poorly resolved. |
| 8 | Replace | Artillery: repeated giant tubes, adjacent rounded objects and carriage parts do not resolve into intelligible loading or recoil mechanisms; excessive flame columns obscure rather than explain the equipment. |
| 9 | Review | Street fight: central contact hands and background grappling figures are ambiguous. |
| 10 | Retain provisionally | Dockyard: strong overall spatial composition; small workers and hoist details need source checking. |
| 11 | Review | Earthwork assault: right foreground rifle grip and the background stock/sling cluster are confused; several combat interactions feel posed rather than connected. |
| 12 | Review | Rooftop fight: footing, roof depth and right-hand rifle struggle are weakly resolved. |
| 13 | Replace | Lamplighter: figure and post float above a city-scale drop without a credible ledge or mounting location; leg support and intended working action are unconvincing. |
| 14 | Retain provisionally | Interior gathering: main silhouettes and objects remain readable; minor faces are simplified. |
| 15 | Retain provisionally | Mounted prairie group: clear principal horse/rider relationships; distant detail is appropriately subordinate. |
| 16 | Review | Steamship departure: foreground waving hands and ship-side crowd blur into repeated forms. |
| 17 | Review | Airships: coherent broad silhouettes, but gondola/propulsion details and intended date need a documented reference. |
| 18 | Retain provisionally | Coffeehouse: plausible overall grouping; faces and newspaper grips are soft but not a clear structural failure. |
| 19 | Retain provisionally | Legacy military painting: clearly differentiated figures; technical issue is its presence outside the current source set, not an identified visual defect. |
| 20 | Review | Sailing battle: gunfire, stern geometry and rigging need a vessel reference before approval. |
| 21 | Replace | Courtyard melee: central crossing weapons and grips are hard to assign; prone foreground figure and the person restraining him merge into an unclear body arrangement. |
| 22 | Retain provisionally | Night gathering: readable central group and lighting; exact depicted event is undocumented. |
| 23 | Retain provisionally | Quiet interior: principal poses are readable; reclining hand and small props remain soft. |
| 24 | Retain provisionally | City street: coherent broad perspective; distant pedestrians are painterly rather than individually resolved. |
| 25 | Replace | Factory injury: injured worker and helpers form a tangled central cluster; hands, wrist/forearm contacts and the treatment action cannot be read reliably. |
| 26 | Review | Religious gathering: foreground backs read clearly, but raised figure, platform and city are generic without subject provenance. |
| 27 | Review | Urban unrest: several foreground/background crowd bodies blend into each other; statue and setting need identification. |
| 28 | Retain provisionally | Prairie railway: simple, readable composition; no obvious primary anatomy failure at review scale. |
| 29 | Review | Caravan: overlapping camel heads, packs and riders need separate anatomical and tack checks. |
| 30 | Review | Door breach: central raised tool, two-handed grip and intended strike are insufficiently clear; other principal figures read better. |
| 31 | Retain provisionally | Monastery: clear major poses and setting; exact place and dress remain unverified. |
| 32 | Review | Assembly: repeated faces and fezzes become formulaic; lower-left heads are partly swallowed by furniture. |
| 33 | Review | Dancer: bent wrist, raised foot and weight distribution need source comparison; do not infer extra limbs merely from the dynamic pose. |
| 34 | Retain provisionally | Oil derricks: readable industrial landscape; engineering details and place are not authenticated. |
| 35 | Review | Harvest: foreground tool shafts and gripping hands need validation against the depicted agricultural action. |
| 36 | Review | Armoured train: turret, chassis and wheel relationships require a real vehicle reference; design currently reads as generic fantasy machinery. |
| 37 | Replace | Street violence: victim's raised arms, captors' grips and adjacent weapon shafts overlap into an ambiguous central tangle; the principal action needs rebuilding. |
| 38 | Review | Locomotive: running gear, track contact and carriage alignment need a documented locomotive reference. |
| 39 | Retain provisionally | Infantry rear view: clear grouping; exact helmet, uniform and firearm details are not historically authenticated. |
| 40 | Review | Machinery hall: large wheels and supports look plausible at a glance, but drive connections and shaft relationships are unresolved. |
| 41 | Review | Military ceremony: horse legs, mounted seating and central presented object need closer reference checking. |
| 42 | Review | Exhibition interior: excessive blur in almost every human figure; weak focal subject and detail readability. |
| 43 | Retain provisionally | Caravan gateway: clear main composition; camel load and small background figures are soft. |
| 44 | Retain provisionally | Two seated dignitaries: readable poses and tea setting; gesturing fingers and costume identity need source verification. |
| 45 | Review | Meeting: prominent pointing hands and surrounding faces are uneven; paper and grip lack convincing detail. |
| 46 | Retain provisionally | Troops in gorge: atmospheric and readable; distant ranks are simplified. |
| 47 | Retain provisionally | Central Asian market: clear architecture-led composition; architectural identity and lettering need source checking. |
| 48 | Review | Cavalry: middle riders and horse bodies overlap ambiguously; validate leg count, saddle seating and reins individually. |
| 49 | Retain provisionally | Street procession: main poses read adequately; raised implement and exact event remain unverified. |
| 50 | Review | Court audience: right guards' sword grips, hands and repeated uniform forms need refinement. |
| 51 | Review | Printing works: large machine lacks clearly readable paper path and working connections; work gestures are generic. |
| 52 | Replace | Firing line: foreground rifles break into wedge-like stocks and blade-like extensions; hands fail to form convincing grips and overlapping weapons cannot be traced consistently. |
| 53 | Review | Prospectors: tool head, shaft and working target do not clearly communicate the action. |
| 54 | Retain provisionally | City panorama: comparatively strong architecture-led screen; exact location remains unverified. |
| 55 | Review | Resting soldiers: foreground dangling hands are elongated and poorly articulated; rifle holding is stiff, though bodies remain readable. |
| 56 | Retain provisionally | Political gathering: main faces and silhouettes read; identities and costume accuracy require references. |
| 57 | Review | Street confrontation: small pistol mechanism and grip are poorly resolved; foreground cane/hand junction is awkward. |
| 58 | Review | Parade: repeated near-identical faces, rigid hands and formulaic marching poses undermine naturalism. |
| 59 | Review | Barricade: raised weapon, standing figure's footing and lower-right combatants are unclear. |
| 60 | Retain provisionally | Harbour sunset: coherent scenery and ship silhouette; no obvious primary anatomy issue. |
| 61 | Retain provisionally | Throne room: readable spatial arrangement; small hands, insignia and identity remain unverified. |
| 62 | Review | Forest gunmen: right figure's carried firearm is obscured and awkwardly integrated into the arm; raised fingers and visible revolver need close source checking. |
