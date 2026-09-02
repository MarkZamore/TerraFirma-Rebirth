# TerraFirma Rebirth

TerraFirma: Rebirth by MerMerrr, release `1.21.1-4.1.21release`, for Minecraft
1.21.1 on NeoForge 21.1.248, laid out as a portable pack the LANMinecraft
launcher can install and update.

The tree is the CurseForge release. Its manifest names 195 mods by project and
file id; 187 came from CurseForge and five more - EntityCulling, 3D Skin
Layers, Create Aeronautics, TFC Sable Rivers and E33 Chat - from Modrinth,
because their authors switched off API distribution on CurseForge and Modrinth
serves the same file names. Seven further mods ride inside the release's own
`overrides/mods`, so the folder holds 199.

Three are still missing and the pack will not run without them. Their authors
blocked API distribution and they are on CurseForge alone, so they have to be
fetched by hand:

| file | page |
| --- | --- |
| `coralstfc-1.21.1-neoforge-1.0.3.jar` | [corals-tfc](https://www.curseforge.com/minecraft/mc-mods/corals-tfc/files/7883936) |
| `tfcorewashing-1.21.1-neoforge-1.1.4.jar` | [tfc-ore-washing](https://www.curseforge.com/minecraft/mc-mods/tfc-ore-washing/files/8058503) |
| `simulatedcoasters-0.1.5.jar` | [create-coasters-simulated](https://www.curseforge.com/minecraft/mc-mods/create-coasters-simulated/files/8655742) |

## What comes from the release and what does not

`config/`, `kubejs/`, `shaderpacks/`, `journeymap/`, `global_packs/` and
`ambience_music/` are the release's own overrides, and its root `options.txt`
is `configureddefaults/options.txt` here, which is where the launcher seeds an
instance from. The client jar is Mojang's own 1.21.1, byte for byte the one the
other packs carry.

`servers.dat` is left out. It is a player's server list, not something the pack
decides.

`ambience_music/` is 380 MB of the 838, and `global_packs/` carries the
resource packs the Global Packs mod force-loads - including a Chinese mod
translation of 1092 files, which is the author's and does nothing to a player
reading anything else. Both are roots the template's publisher did not know
about, so `tools/generate_manifest.py` names them: a root missing from
`SCAN_ROOTS` is never published, and the pack would arrive quietly short.

## The questbook is already Russian

FTB Quests, 36 chapters, and the release ships
`config/ftbquests/quests/lang/ru_ru.snbt` alongside English, Spanish and
Chinese. It is complete: the same 1958 keys as `en_us.snbt`, none missing in
either direction, and Cyrillic in 1214 of its 1231 strings. Nothing here
translates anything - the work is the author's, and it only had to be carried
through rather than dropped.

`options.txt` sets no language, so the game opens in English and follows
whatever the player picks; the questbook follows with it.

## Publishing

`tools/generate_manifest.py` writes `pack-manifest.json` and stages the zipped
roots; `.github/workflows/publish.yml` runs it on every push to `main` and
rolls the `pack-latest` release. The manifest carries `modCount` - jars plus
the mods nested inside them - so the launcher's memory estimate reads the same
before the download and after.
