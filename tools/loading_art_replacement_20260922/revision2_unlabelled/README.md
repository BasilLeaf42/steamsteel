# Installed loading artwork — wide crop revision

61 oil paintings plus the original Plevna surrender screen (slot 19), restored byte-for-byte at the user's request.

The paintings fill the original 1024×490 artwork panel edge to edge. Each crop has a recorded subject-specific position and has been visually inspected. Eight unsuitable compositions were replaced with other paintings. The original lower 278 rows remain unchanged in each 1024×768 RGBA RLE TGA texture.

- `gallery.html`: current full-width crops, original comparisons, source links and crop reasons.
- `ARTWORK_CREDITS.md`: current artists, dates, licences, subject differences and medium evidence.
- `source_register.json`: final crop boxes, hashes and visual review.
- `installation_manifest.json`: all 186 verified installed files and before/after hashes.
- `archive/original_members.json`: the original pre-replacement assets and their member paths.
- `revision1/`: previous fitted paintings and installation metadata, retained for rollback.

The installation covers runtime, `load_steamsteel` and `load_althis`. Pixel comparisons verified that every artwork panel exactly matches its approved resized crop, with no generated fill, border or mat. All lower text areas match their originals; Plevna matches its entire archived original. The game was not launched for an engine-level check.

For rollback, first compare current files to the installation manifest to protect later edits. The manifest records the prior installation archive for every file; the original archive retains the assets from before either replacement pass.
