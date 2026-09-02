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

## The shader is the player's to fetch

`shaderpacks/` carries two `.txt` files named for Complementary. They are not
shaders - they are Euphoria Patches settings files, and the first line of each
says so. The shader itself is not here and cannot be: Complementary's licence
allows a modpack to include it only "by using Modrinth or CurseForge's existing
systems", and says plainly that redistributing it "using a direct file upload"
is not allowed. This pack is files in a git repository, which is exactly that.

So `EuphoriaPatcher` says `SHADER NOT FOUND` until the player puts one in. The
mod here is `EuphoriaPatcher-1.10.0-r5.9-neoforge.jar`, so the version that matches is
**r5.9**:

- [Complementary Reimagined r5.9](https://modrinth.com/shader/complementary-reimagined/version/r5.9)
- [Complementary Unbound r5.9](https://modrinth.com/shader/complementary-unbound/version/r5.9)

Drop either zip into `shaderpacks/` and Euphoria Patches builds the patched
version beside it. The release shipped EuphoriaPatcher 1.9.3 with r5.8.1, and that pair does not
compile under the Iris this pack also ships. Stock Complementary r5.8.1 loads
fine on the same Iris, so what Iris chokes on is what the patcher adds:

    final.fsh: ERROR: 0:854: '_10' : undeclared identifier

`_10` is a name Iris's own translator generates and then fails to declare, so
the fault is in the pairing rather than in anybody's shader source. Iris cannot
move: it is 1.8.14-beta.1 because that is the one that speaks Sodium 0.8, this
pack ships Sodium 0.8.13-beta.1, and Sable declares anything below
0.8.12-alpha.2 incompatible. So the patcher moved instead - to 1.10.0-r5.9,
which the mod itself asked for. The author's three shader settings were carried
across into files named for the new pair.

`TFCR-Bliss` and `TFCR-photon-voxy-support` are shipped and work without any of
this.

The pack's `config/iris.properties` names the shader it starts with, and it
named the old one - `TFCR-ComplementaryReimagined_r5.8.1 + EuphoriaPatches_1.9.3`,
a folder that no longer gets built. It names the new pair now. Iris still opens
with shaders on, as the author had it; a player who has not fetched the base
shader yet simply has nothing at that name, which was already true of the old
one.

`config/euphoria_patcher/.data.json` went with it. That file is the patcher's
own record of what it last built - a version and the hash of the base shader it
was built from - and shipping one that describes r5.8.1 could talk the patcher
out of rebuilding. It writes a fresh one on the first run.

## One warning removed

`config/fml.toml` held `sable = ["-scalablelux"]`, softening Sable's declared
incompatibility with ScalableLux. ScalableLux is not in this pack, so the
override matched nothing and NeoForge said so on every load - the one warning
on the mod-loading screen. It is gone.

The file is claimed in `launcher/pack-owned.txt`, because NeoForge rewrites it
itself: it looks player-edited from the first launch, and nothing shipped could
otherwise reach an instance that already has it.

## Publishing

`tools/generate_manifest.py` writes `pack-manifest.json` and stages the zipped
roots; `.github/workflows/publish.yml` runs it on every push to `main` and
rolls the `pack-latest` release. The manifest carries `modCount` - jars plus
the mods nested inside them - so the launcher's memory estimate reads the same
before the download and after.
