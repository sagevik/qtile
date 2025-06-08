import os
import subprocess

from libqtile.lazy import lazy

SCRIPTS_PATH = "~/.config/qtile/scripts"


def autostart() -> None:
    # os.environ["XDG_SESSION_TYPE"] = "wayland"
    # os.environ["XDG_CURRENT_DESKTOP"] = "wlroots"
    autostart = os.path.expanduser(f"{SCRIPTS_PATH}/autostart.sh")
    subprocess.Popen([autostart])


@lazy.function
def lock_qtile(_qtile):
    subprocess.run(["swaylock", "-i", "~/Pictures/Wallpapers/austria.jpg", "--clock"])


@lazy.function
def power_menu(_qtile) -> None:
    power_menu = os.path.expanduser(f"{SCRIPTS_PATH}/rofi-power.py")
    subprocess.Popen([power_menu])


@lazy.function
def wifi_menu(_qtile) -> None:
    wifi_menu = os.path.expanduser(f"{SCRIPTS_PATH}/rofi-wifi.sh")
    subprocess.Popen([wifi_menu])


# TODO: check if working
@lazy.function
def bluetooth_menu(_qtile) -> None:
    bluetooth_menu = os.path.expanduser(f"{SCRIPTS_PATH}/rofi-bt.sh")
    subprocess.Popen([bluetooth_menu])
