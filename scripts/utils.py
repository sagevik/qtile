import subprocess
import re

from libqtile import qtile
from libqtile.lazy import lazy


def get_audio_output_device():
    sink = subprocess.run(
        ["pactl", "get-default-sink"], capture_output=True, text=True
    ).stdout.strip()

    sinks_out = subprocess.run(
        ["pactl", "list", "sinks"], capture_output=True, text=True
    ).stdout

    # Isolate the block for the current sink
    match = re.search(rf"(?s)Name: {re.escape(sink)}\n(.*?)(?=\nName:|\Z)", sinks_out)
    if not match:
        return "Audio: Unknown"

    block = match.group(1)

    port_match = re.search(r"Active Port:\s*(\S+)", block)
    if not port_match:
        return "Audio: Unknown"

    port = port_match.group(1)
    pretty = port.replace("analog-output-", "").replace("-", " ").title()

    return pretty


def shift_group(qtile, direction):
    groups = qtile.groups
    current_group = qtile.current_group
    idx = [group.name for group in groups].index(current_group.name)
    new_idx = (idx + direction) % len(groups)
    qtile.current_window.togroup(groups[new_idx].name)
    if direction == 1:
        lazy.screen.next_group()
    else:
        lazy.screen.prev_group()


def floating_to_front(qtile):
    w = qtile.current_window
    if w.floating:
        w.bring_to_front()


def blueman_manager():
    return {"Button1": lambda: qtile.cmd_spawn("blueman-manager")}


def select_wifi(config_dir):
    return {"Button1": lambda: qtile.cmd_spawn(f"{config_dir}/qtile/scripts/wifi.sh")}


def get_package_updates():
    try:
        with open("/tmp/packageUpdates", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "X"


def run_updates(qtile):
    updates = get_package_updates()
    if updates == "0":
        qtile.cmd_spawn(subprocess.run(["notify-send", "Archupdate", "No updates"]))
    else:
        qtile.cmd_spawn("ghostty -e archupdate")
