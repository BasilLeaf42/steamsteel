Steam & Steel packed SSK vertical launch-point fix
Built: 2026-09-15

Correct coordinate order:
  lateral, vertical height, forward
  original: 0.1888, 1.4974, 1.3438
  corrected: 0.1888, 0.6474, 1.3438
  vertical delta: -0.85

Install only while M2EX/Medieval II is closed:
  Copy skeletons.dat and skeletons.idx to data\animations.
  Leave pack.dat and pack.idx unchanged.
  Remove data\animations\aninterp.cache before the next launch.

Verification:
  161/161 archive members re-extracted.
  skeletons.idx is byte-identical to the original.
  skeletons.dat differs at exactly three byte positions within one float.
  Only MTW2_Musket_SSK.bin differs, at float offset 7828.

Rollback backups are recorded in tools\ssk_launchpoint_fix.json.
