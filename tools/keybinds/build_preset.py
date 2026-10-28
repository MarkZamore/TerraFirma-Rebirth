#!/usr/bin/env python3
"""Build the complete TerraFirma Rebirth controls preset from its verified registry.

Run scan_keys.py after changing mods, review the registry and layout, then run
this script followed by check_preset.py. --check verifies reproducibility without
writing anything. Inputs and output are UTF-8; no player options are edited.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
K = "key.keyboard."
M = "key.mouse."
UNBOUND = K + "unknown"

# Every normal vanilla control keeps its standard key. Creative toolbar keys
# and Social Interactions are released for chisel/tool swap/jetpack controls.
VANILLA = {
    "key.attack": M + "left", "key.use": M + "right",
    "key.forward": K + "w", "key.left": K + "a", "key.back": K + "s", "key.right": K + "d",
    "key.jump": K + "space", "key.sneak": K + "left.shift", "key.sprint": K + "left.control",
    "key.drop": K + "q", "key.inventory": K + "e", "key.chat": K + "t",
    "key.playerlist": K + "tab", "key.pickItem": M + "middle", "key.command": K + "slash",
    "key.socialInteractions": UNBOUND, "key.screenshot": K + "f2", "key.togglePerspective": K + "f5",
    "key.smoothCamera": UNBOUND, "key.fullscreen": K + "f11", "key.spectatorOutlines": UNBOUND,
    "key.swapOffhand": K + "f", "key.saveToolbarActivator": UNBOUND, "key.loadToolbarActivator": UNBOUND,
    "key.advancements": K + "l",
    **{f"key.hotbar.{n}": K + str(n) for n in range(1, 10)},
}

LAYOUT = {
    # TFC's three core controls remain reachable from WASD.
    "tfc.key.place_block": K + "v",
    "tfc.key.cycle_chisel_mode": K + "c",
    "tfc.key.stack_food": K + "i",
    "key.sophisticatedbackpacks.open_backpack": K + "b",
    "key.sophisticatedbackpacks.tool_swap": K + "x",
    "key.sophisticatedbackpacks.inventory_interaction": K + "j",
    "key.curios.open.desc": K + "g",
    "key.astikorcartsredux.action": K + "h",
    "key.astikorcartsredux.slow": K + "z",
    "key.jei.showRecipe": K + "r", "key.jei.showUses": K + "u", "key.jei.bookmark": K + "y",
    "key.jei.recipeBack": K + "backspace",
    "key.jei.previousRecipePage": K + "page.up", "key.jei.nextRecipePage": K + "page.down",
    "key.jei.closeRecipeGui": K + "escape",
    "key.journeymap.map_toggle_alt": K + "m",
    "key.journeymap.create_waypoint": K + "n",
    "key.journeymap.zoom_in": K + "equal", "key.journeymap.zoom_out": K + "minus",
    "iris.keybind.toggleShaders": K + "k", "iris.keybind.shaderPackSelection": K + "o",
    "iris.keybind.reload": K + "f6",
    "key.modernui.openCenter": K + "f8", "key.modernui.zoom": M + "4",
    "key.corpse.death_history": K + "f9",
    "tfcgenviewer.key.open_viewer": K + "f10",
    "key.unlockIME": K + "f12",
    "key.rocketnautics.toggle_jetpack": K + "p",
    "key.rocketnautics.toggle_dampeners": K + "home",
    "key.rocketnautics.toggle_alignment": K + "end",
    "create.keyinfo.toolbelt": K + "caps.lock", "create.keyinfo.toolmenu": K + "menu",
    "create.keyinfo.rotate_menu": K + "backslash",
    "create.keyinfo.shift_modifier": K + "right.shift",
    "create.keyinfo.ctrl_modifier": K + "right.control",
    "create.keyinfo.alt_modifier": K + "right.alt",
    "key.ponder.ponder": K + "f4",
    "key.jade.show_details": K + "left.alt",
    "key.sophisticatedcore.sort": K + "semicolon",
    "key.sophisticatedcore.transfer_to_storage": K + "left.bracket",
    "key.sophisticatedcore.transfer_to_inventory": K + "right.bracket",
    "key.tracks.open_tuning": K + "comma",
    "key.immersiveengineering.magnetEquip": K + "f7",
    "key.immersiveengineering.railgunZoom": K + "period",
    "key.immersiveengineering.chemthrowerSwitch": K + "0",
    "key.sable_schematic_api.blueprint_tool.open": K + "insert",
    "key.sable_schematic_api.camera.open": K + "delete",
    "key.aero_cam_sync.toggle": K + "down",
    "key.climbable_ropes.lock_rope_camera": K + "pause",
    "key.aeroworks.joystick.free_camera": M + "5",
    "key.dashpanels.hold_move_camera": K + "up",
    "key.dashpanels.hold_to_open_wiki": K + "apostrophe",
    "simulated.keyinfo.rotate_mode": K + "right",
    "key.ftbquests.quests": K + "grave.accent",
    "key.ftbquests.gui.extended_info": K + "f1",
    "key.journeymap.minimap_toggle_alt": K + "scroll.lock",
}


def render() -> str:
    with (HERE / "registered-keys.tsv").open(encoding="utf-8") as registry:
        rows = [r for r in csv.DictReader(registry, delimiter="\t")
                if {"options", "jar"} & set(r["seen"].split("+"))]
    registered = {r["name"] for r in rows}
    missing = (set(VANILLA) | set(LAYOUT)) - registered
    if missing:
        raise ValueError("Layout names unregistered mappings: " + ", ".join(sorted(missing)))
    lines = [
        "# TerraFirma Rebirth controls preset: TFC, exploration and engineering.",
        "# Applied only by the launcher controls-preset button; never automatically.",
        "# Complete registered mapping list; unassigned keys are explicit.",
        "# Generated by tools/keybinds/build_preset.py. See tools/keybinds/design.md.",
    ]
    last_mod = None
    for row in sorted(rows, key=lambda r: (r["name"] not in VANILLA, r["mod"], r["name"])):
        name = row["name"]
        mod = "Minecraft" if name in VANILLA else (row["mod"] or "Other")
        if mod != last_mod:
            lines.extend(["", "# --- " + mod + " ---"])
            last_mod = mod
        value = VANILLA.get(name, LAYOUT.get(name, UNBOUND))
        label = row["english"] or name
        lines.append(f"key_{name}:{value}  # {label}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    destination = REPO / "launcher" / "controls-preset.txt"
    output = render()
    if args.check:
        if not destination.exists() or destination.read_bytes() != output.encode("utf-8"):
            print("Preset differs from its generator; run build_preset.py")
            return 1
    else:
        destination.write_text(output, encoding="utf-8", newline="\n")
    print(f"Verified {sum(line.startswith('key_') for line in output.splitlines())} mappings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
