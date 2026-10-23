# Official mod project pages

`mod-pages.json` maps each stable mod ID from the shipped jars to the official project page.
The library generator writes it as `websiteUrl`, for gameplay mods, addons and libraries alike.
A new mod without a verified HTTPS project page fails metadata generation.

Use CurseForge first; if the same project is not published there, use Modrinth;
otherwise use its author's official website or source/release repository.
Match the actual jar/hash and author, especially for forks and similarly named projects.
Never guess a slug, substitute an unrelated project, or link to search results, mirrors,
issue trackers or direct jar downloads. A bundled component with no standalone project
may link to the original author's pack; record that exception explicitly.

Page lookup belongs to catalogue preparation. Launcher navigation and clicks do not
search hosting sites, check updates, download game files or change the active pack.
After changing a jar or adding a pack, update the mapping and run the generator tests
and a fresh build from actual jars. Do not commit API keys or private cache files.

Unavailable author pages are explicit objects: `{ "url": "https://…", "available": false }`.
The last known author URL is retained for provenance, while the launcher renders plain text.

## Bundled components without standalone project pages

`catalyst` (Rohan Verma) and `deployer_got_dizzy` (enxv233) are distributed inside the original TerraFirma Rebirth release. Their links use its official CurseForge pack page; similarly named standalone projects belong to different authors.
