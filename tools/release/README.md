# Steam & Steel release builder

Before each build, `Sync-M2EXRuntime.ps1` uses the verified `M2EX.7z` distribution as a path allow-list, then stages the corresponding files from the maintainer's current Medieval II root. This includes the relevant root runtime, `data`, `packs`, and `miles` files while excluding bundled mod copies, development tools, symbols, and debug libraries. Taking bytes from the current installation deliberately preserves accepted M2EX fixes and other developer deviations from the base archive.

This directory defines the public release independently of the development tree. The builder creates a new staging directory outside the repository and never deletes development files.

## Build a prerelease staging directory

```powershell
powershell -ExecutionPolicy Bypass -File tools/release/Build-SteamSteelRelease.ps1 -Version 1.2 -AuditDuplicates
```

## Build and test the final 7-Zip archive

```powershell
powershell -ExecutionPolicy Bypass -File tools/release/Build-SteamSteelRelease.ps1 -Version 1.2 -AuditDuplicates -CreateArchive
```

To apply a reviewed patch overlay while packaging, pass `-PatchDirectory <folder>`. Its contents must use paths relative to the mod root (for example `data/...`). The overlay is applied before the final manifest, installer compilation, compression and archive test, so the recorded hashes describe the actually shipped files.

The default output is the sibling directory `mods/steamsteel-release-builds`, outside the live mod and Git working tree. Each package contains `Steam_and_Steel_Setup.exe` beside `payload/steamsteel`. Keep that layout intact: the installer deliberately uses an external payload so it is not constrained by the Windows executable-size limit.

The installer detects the standard Steam installation and additional Steam library folders, accepts a manually selected compatible installation, validates `medieval2.exe` and the base `data` directory, installs only under `mods/steamsteel`, creates optional shortcuts, and supports uninstall bookkeeping.

This is deliberately a clean-install package. When `mods/steamsteel` already exists, the interactive installer warns that saves, preferences, backups, and personal files inside it will be lost and requires explicit confirmation. Immediately before extraction it revalidates the selected Medieval II directory, deletes the complete old `mods/steamsteel` tree, and aborts if either validation or deletion fails. Silent installation cannot purge an existing copy because it cannot obtain that confirmation.

The Finish page also offers an unchecked cleanup action. When selected after a successful installation, it waits for Setup to exit and removes only the adjacent `payload` directory, the exact running Setup executable, and `Steam_and_Steel_<version>.7z` when that exact archive is in the same directory. It does not delete unrelated archives or any installed mod files.

The external payload also contains the four non-system x64 libraries directly imported by the M2EX launcher (`steam_api64.dll`, `mss64.dll`, `binkw64.dll`, and `granny2_x64.dll`). Setup installs a missing copy into the Medieval II root without overwriting or uninstalling an existing shared copy. The Microsoft-signed x64 Visual C++ Redistributable is run in passive no-restart mode to supply the supported MSVC/MFC runtime. Shortcuts launch from the game root and pass `@mods\steamsteel\steamsteel.cfg`, matching the working launch path used by the batch file.

Edit `release-allowlist.json` when a new runtime root or root-level file is genuinely required. Do not convert the allowlist into a broad exclusion-only copy. Identical files at different paths are reported but retained because the engine may require each path.

The build fails if a newly added directory inside a runtime root has a development-like name such as `backup`, `source`, `preview`, `staged`, or `cache` and it has not been explicitly handled. This prevents future work products from silently entering a prerelease.

The output manifest records every included path, size and SHA-256 hash, the Git commit, whether the working tree was dirty, and the allowlist hash. Archive creation uses 7-Zip's supported Ultra preset (`-mx=9`) with solid LZMA2 and a four-thread cap to prevent pagefile exhaustion on high-core systems. It also tests the completed archive and writes `SHA256SUMS.txt`.
