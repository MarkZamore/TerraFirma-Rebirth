# TerraFirma Rebirth

TerraFirma: Rebirth by MerMerrr, release `1.21.1-4.1.21release`, for Minecraft
1.21.1 on NeoForge 21.1.248, laid out as a portable pack the LANMinecraft
launcher can install and update.

The tree is the CurseForge release. Its manifest names 195 mods by project and
file id; 187 came from CurseForge and five more - EntityCulling, 3D Skin
Layers, Create Aeronautics, TFC Sable Rivers and E33 Chat - from Modrinth,
because their authors switched off API distribution on CurseForge and Modrinth
serves the same file names. Seven further mods ride inside the release's own
`overrides/mods`, so the folder holds 199 before the three below.

Three more came from CurseForge by hand, because their authors blocked API
distribution and they exist nowhere else - `coralstfc` 1.0.3, `tfcorewashing`
1.1.4 and `simulatedcoasters` 0.1.5, each checked against the SHA-1 CurseForge
publishes for it. So the folder held 202; one came back out, for the reason below.

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

## CustomSkinLoader is out

The release shipped CustomSkinLoader 15.0.1 and the game would not start with
it:

    Patch 'customskinloader:skin-manager-patch:skin-manager.<init>.v1'
    matched protocol 0 but did not modify any bytecode

It patches `net.minecraft.client.resources.SkinManager`, and so does the
launcher's identity agent - `createSkinLookup` and the lambda inside it are
named in the arguments every launch is given. The agent is a `-javaagent`, so
it runs before ModLauncher's transformers; by the time CustomSkinLoader looks
at the constructor it is no longer the shape it expects, and it refuses rather
than guess.

Two skin systems cannot both own that class, and the launcher's is the one this
whole setup rests on: skins follow a player across machines and across a LAN
from their Steam identity. CustomSkinLoader answers the same question for skin
servers this setup does not use, and nothing in the pack declares it - no mod
here names it as a dependency. So it is out rather than silenced with
`-Dcustomskinloader.ignorePatchFailure=true`, which would have let the game
start with the mod loaded and its one job undone.

mods/ holds 201.

## Publishing

`tools/generate_manifest.py` writes `pack-manifest.json` and stages the zipped
roots; `.github/workflows/publish.yml` runs it on every push to `main` and
rolls the `pack-latest` release. The manifest carries `modCount` - jars plus
the mods nested inside them - so the launcher's memory estimate reads the same
before the download and after.
