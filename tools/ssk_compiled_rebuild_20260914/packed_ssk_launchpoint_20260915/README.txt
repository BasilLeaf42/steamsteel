Steam & Steel packed SSK launch-point fix
Built: 2026-09-15

Install only while M2EX/Medieval II is closed:
  Copy skeletons.dat and skeletons.idx to data\animations.
  Leave pack.dat and pack.idx unchanged.
  Remove data\animations\aninterp.cache before the next launch.

Effect:
  MTW2_Musket_SSK attack_missile_release height 1.3438 -> 0.4938 (-0.85).
  Projectile, muzzle flash, and smoke share this compiled release origin.

Verification:
  161/161 archive members re-extracted.
  skeletons.idx is byte-identical to the original.
  skeletons.dat differs at exactly four bytes.
  Only MTW2_Musket_SSK.bin differs, at float offset 7832.

Rollback:
  Restore skeletons.dat and skeletons.idx from:
  tools\animation_archive_backup_before_packed_ssk_activation_20260915
  Then remove aninterp.cache before relaunching.

Full hashes and byte audit: tools\ssk_launchpoint_fix.json
