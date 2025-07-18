import os
import subprocess

from libqtile import bar, widget, qtile

from assets.constants import FONT_SIZE, FONT_TYPE, Colours
# from scripts.utils import get_audio_output_device

config_dir = os.environ.get("XDG_CONFIG_HOME")


def is_using_x11():
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if session_type == "wayland":
        return False
    elif session_type == "x11":
        return True

    if os.environ.get("WAYLAND_DISPLAY"):
        return False

    if os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        return True

    return True


def blueman_manager():
    return {"Button1": lambda: qtile.cmd_spawn("blueman-manager")}


def select_wifi():
    return {"Button1": lambda: qtile.cmd_spawn(f"{config_dir}/qtile/scripts/wifi.sh")}


def get_package_updates():
    try:
        with open("/tmp/packageUpdates", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "X"


def run_updates():
    updates = get_package_updates()
    if updates == "0":
        qtile.cmd_spawn(subprocess.run(
            ["notify-send", "Archupdate", "No updates"]
        ))
    else:
        qtile.cmd_spawn("ghostty -e archupdate")


def my_systray():
    return widget.StatusNotifier(
        icon_theme="Breeze",
        padding=5,
        icon_size=FONT_SIZE,
    )


def spacer(size: int = 2):
    return widget.Spacer(
        length=size,
        background=Colours.BLACK,
    )


def get_bar_widgets(with_systray=False):
    widgets = [
        widget.GroupBox(
            fontsize=FONT_SIZE,
            borderwidth=2,
            highlight_method="block",
            active=Colours.WHITE,
            block_highlight_text_color=Colours.BLACK,
            # block_highlight_text_color=Colours.YELLOW,
            inactive=Colours.BLUE_GREY,
            background=Colours.BLACK,
            this_current_screen_border=Colours.WHITE,
            # this_current_screen_border=Colours.BLUE_GREY,
            this_screen_border=Colours.BLACK,
            other_current_screen_border=Colours.GREY,
            other_screen_border=Colours.BLACK,
            urgent_border=Colours.DARK_BLUE,
            rounded=True,
            disable_drag=True,
            font=FONT_TYPE,
        ),
        spacer(),
        widget.Image(
            filename="~/.config/qtile/assets/graphics/layout.png",
            background=Colours.BLACK,
        ),
        widget.CurrentLayout(
            background=Colours.BLACK,
            foreground=Colours.GREY,
            fmt="{}",
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
        ),
        spacer(),
        widget.TextBox(
            background=Colours.BLACK,
            foreground=Colours.WHITE,
            text="|",
        ),
        spacer(),
        widget.WindowName(
            background=Colours.BLACK,
            format="{name}",
            font=FONT_TYPE,
            foreground=Colours.WHITE,
            empty_group_string="Desktop",
            fontsize=FONT_SIZE,
        ),
        # Right side
        widget.TextBox(
            background=Colours.BLACK,
            foreground=Colours.WHITE,
            text="   :",
            font=FONT_TYPE,
            fontsize=FONT_SIZE+2,
        ),
        widget.TextBox(
            background=Colours.BLACK,
            foreground=Colours.WHITE,
            text=" ",
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
        ),
        widget.GenPollText(
            update_interval=1800,
            func=get_package_updates,
            fmt="{}",
            foreground=Colours.WHITE,
            background=Colours.BLACK,
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
            mouse_callbacks={"Button1": lambda: run_updates()}
        ),
        spacer(8),
        widget.Image(
            filename="~/.config/qtile/assets/graphics/wifi.png",
            # filename="~/.config/qtile/assets/graphics/internet.png",
            background=Colours.BLACK,
            margin_y=8,
            mouse_callbacks=select_wifi()
        ),
        spacer(4),
        widget.Wlan(
            format="{essid} [{percent:2.0%}]",
            # font="Hack Nerd",
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
            interface="wlan0",
            background=Colours.BLACK,
            mouse_callbacks=select_wifi()
        ),
        spacer(4),
        widget.Image(
            filename="~/.config/qtile/assets/graphics/bluetooth.svg",
            background=Colours.BLACK,
            margin_y=6,
            mouse_callbacks=blueman_manager()
        ),
        widget.Bluetooth(
            hci="/org/bluez/hci0",  # Adjust to your Bluetooth device
            experimental=True,
            padding=2,
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
            background=Colours.BLACK,
            mouse_callbacks=blueman_manager()
            # mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("blueman-manager")}
        ),
        spacer(),
        widget.GenPollText(
            # update_interval=1,
            name="barvolume",
            func=lambda: subprocess.check_output("volume").decode().strip(),
            background=Colours.BLACK,
            foreground=Colours.WHITE,
            font=FONT_TYPE,
            fontsize=FONT_SIZE+2,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("pavucontrol")}
        ),
        widget.Image(
            margin_y=2,
            margin_x=2,
            filename="~/.config/qtile/assets/graphics/cpu.png",
            background=Colours.BLACK,
        ),
        widget.CPU(
            format="{load_percent}%",
            foreground=Colours.WHITE,
            background=Colours.BLACK,
            min_chars=6,
            fontsize=FONT_SIZE,
            max_chars=6,
        ),
        spacer(4),
        widget.Image(
            margin_y=4,
            margin_x=2,
            filename="~/.config/qtile/assets/graphics/ram.png",
            background=Colours.BLACK,
        ),
        widget.Memory(
            background=Colours.BLACK,
            format="{MemUsed: .0f}{mm}",
            measure_mem="G",
            foreground=Colours.WHITE,
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
            update_interval=10,
        ),
        spacer(4),
        widget.BatteryIcon(
            battery="BAT0",
            theme_path="~/.config/qtile/assets/graphics/battery_theme/",
            background=Colours.BLACK,
            scale=1,
        ),
        widget.Battery(
            battery="BAT0",
            font=FONT_TYPE,
            background=Colours.BLACK,
            foreground=Colours.WHITE,
            format="{percent:2.0%}",
            fontsize=FONT_SIZE,
            low_foreground=Colours.WARNING,
            low_percentage=0.2,
        ),
        # widget.Volume(
        #     font=FONT_TYPE,
        #     background=Colours.BLACK,
        #     foreground=Colours.WHITE,
        #     fontsize=FONT_SIZE,
        #     emoji=True,
        #     padding=10,
        # ),
        # spacer(),
        # widget.GenPollText(
        #     update_interval=2,
        #     func=get_audio_output_device,
        #     font=FONT_TYPE,
        #     background=Colours.DARK_BLUE,
        #     foreground=Colours.WHITE,
        #     fontsize=13,
        # ),


        spacer(),
        widget.Clock(
            background=Colours.BLACK,
            foreground=Colours.WHITE,
            font=FONT_TYPE,
            fontsize=FONT_SIZE,
        ),
        spacer(),
    ]
    systray = [
        widget.Systray(
            background=Colours.BLACK,
            foreground=Colours.WHITE,
        ),
    ]
    # for X11
    if with_systray:
        widgets += systray
    return widgets


top_bar = bar.Bar(
    get_bar_widgets(is_using_x11()),
    size=26,
    border_width=[0, 0, 0, 0],
    margin=[0, 0, 0, 0],
)

top_bar2 = bar.Bar(
    get_bar_widgets(),
    size=22,
    border_width=[0, 0, 0, 0],
    margin=[0, 0, 0, 0],
)
