import os
import subprocess

from libqtile.lazy import lazy

SCRIPTS_PATH = "~/.config/qtile/scripts"


def autostart() -> None:
    os.environ["XDG_CONFIG_HOME"] = os.path.expanduser("~/.config")
    autostart = os.path.expanduser(f"{SCRIPTS_PATH}/autostart.sh")
    subprocess.Popen([autostart])


@lazy.function
def power_menu(_qtile) -> None:
    power_menu = os.path.expanduser(f"{SCRIPTS_PATH}/power.py")
    subprocess.Popen([power_menu])


@lazy.function
def wifi_menu(_qtile) -> None:
    wifi_menu = os.path.expanduser(f"{SCRIPTS_PATH}/wifi.sh")
    subprocess.Popen([wifi_menu])


@lazy.function
def bluetooth_menu(_qtile) -> None:
    bluetooth_menu = os.path.expanduser(f"{SCRIPTS_PATH}/bluetooth.py")
    subprocess.Popen([bluetooth_menu])


@lazy.function
def recorder_menu(_qtile) -> None:
    bluetooth_menu = os.path.expanduser(f"{SCRIPTS_PATH}/recorder.py")
    subprocess.Popen([bluetooth_menu])


@lazy.function
def displayselect(_qtile) -> None:
    bluetooth_menu = os.path.expanduser(f"{SCRIPTS_PATH}/displayselect.sh")
    subprocess.Popen([bluetooth_menu])
