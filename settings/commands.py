import os
import subprocess

from libqtile.lazy import lazy
from libqtile.log_utils import logger

SCRIPTS_PATH = "~/.config/qtile/scripts"


class Brightness:
    @staticmethod
    def increase_brightness_cmd() -> str:
        """Increase screen brightness."""
        return "brillo -q -u 200000 -A 5%"

    @staticmethod
    def decrease_brightness_cmd() -> str:
        """Decrease screen brightness."""
        return "brillo -q -u 200000 -U 5%"


class Microphone:
    @staticmethod
    def toggle_microphone_mute_cmd():
        """Toggle microphone on/off"""
        return "pactl set-source-mute @DEFAULT_SOURCE@ toggle"


def setup_mouse(*args) -> None:
    logger.warning(f"[qtile.config] externals_setup called with args: {args}")
    logger.warning("[qtile.config] setting mouse script")
    xinput_script = os.path.expanduser(f"{SCRIPTS_PATH}/mouse.sh")
    subprocess.Popen([xinput_script])


def _external_display_detected() -> bool:
    xrandr_output = subprocess.run(["xrandr"], capture_output=True, text=True)
    return "DP-3-3 connected" in xrandr_output.stdout


def setup_display(*args) -> None:
    logger.warning(f"[qtile.config] externals_setup called with args: {args}")

    xrandr_script = os.path.expanduser(f"{SCRIPTS_PATH}/display.sh")
    commands = [xrandr_script]
    if _external_display_detected():
        commands.append("EXTERNAL")
    subprocess.Popen(commands)


def autostart() -> None:
    autostart = os.path.expanduser(f"{SCRIPTS_PATH}/autostart.sh")
    subprocess.Popen([autostart])


@lazy.function
def power_menu(_qtile) -> None:
    power_menu = os.path.expanduser(f"{SCRIPTS_PATH}/rofi-power.py")
    subprocess.Popen([power_menu])


@lazy.function
def wifi_menu(_qtile) -> None:
    wifi_menu = os.path.expanduser(f"{SCRIPTS_PATH}/rofi-wifi.sh")
    subprocess.Popen([wifi_menu])


@lazy.function
def bluetooth_menu(_qtile) -> None:
    bluetooth_menu = os.path.expanduser(f"{SCRIPTS_PATH}/rofi-bt.sh")
    subprocess.Popen([bluetooth_menu])
