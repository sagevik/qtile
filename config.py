from libqtile import bar, hook, qtile, widget
# from libqtile.backend.wayland import InputConfig
from libqtile.backend.wayland.inputs import InputConfig
from libqtile.config import Click, Drag, DropDown, Group, Key, KeyChord, Match, ScratchPad, Screen
from libqtile.layout.columns import Columns
from libqtile.layout.floating import Floating
from libqtile.layout.max import Max
from libqtile.layout.xmonad import MonadTall, MonadWide
from libqtile.lazy import lazy

from assets.constants import FONT_TYPE, WALLPAPER, Colours

# from scripts.audio import lower_volume, raise_volume, toggle_mute_audio_output
from scripts.menus import (
    autostart,
    bluetooth_menu,
    power_menu,
    recorder_menu,
    wifi_menu,
)
from scripts.screen import decrease_brightness, increase_brightness
# from scripts.utils import shift_group
from top_bar import top_bar, top_bar2

mod = "mod4"
alt = "mod1"
terminal = "ghostty"


@hook.subscribe.startup_once
def on_startup():
    autostart()


keys = [
    # Key([mod, alt], "Left", lazy.screen.prev_group(), desc="Move to previous group"),
    # Key([mod, alt], "h", lazy.screen.prev_group(), desc="Move to previous group"),
    # Key([mod, alt], "Right", lazy.screen.next_group(), desc="Move to next group"),
    # Key([mod, alt], "l", lazy.screen.next_group(), desc="Move to next group"),
    # Key(
    #     [alt, "shift"],
    #     "h",
    #     lazy.function(lambda qtile: shift_group(qtile, -1)),
    #     lazy.screen.prev_group(),
    #     desc="Move window to previous group",
    # ),
    # Key(
    #     [alt, "shift"],
    #     "Left",
    #     lazy.function(lambda qtile: shift_group(qtile, -1)),
    #     lazy.screen.prev_group(),
    #     desc="Move window to previous group",
    # ),
    # Key(
    #     [alt, "shift"],
    #     "l",
    #     lazy.function(lambda qtile: shift_group(qtile, 1)),
    #     lazy.screen.next_group(),
    #     desc="Move window to next group",
    # ),
    # Key(
    #     [alt, "shift"],
    #     "Right",
    #     lazy.function(lambda qtile: shift_group(qtile, 1)),
    #     lazy.screen.next_group(),
    #     desc="Move window to next group",
    # ),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.next(), desc="Move focus next"),
    # Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.previous(), desc="Move focus previous"),
    # Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.next(),
        desc="Move window focus to other window",
    ),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left().when(layout="columns"),
        lazy.layout.grow().when(layout="monadtall"),
        lazy.layout.grow().when(layout="monadwide"),
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right().when(layout="columns"),
        lazy.layout.shrink().when(layout="monadtall"),
        lazy.layout.shrink().when(layout="monadwide"),
    ),
    Key([mod, "control", "shift"], "h", lazy.layout.shrink_left()),
    Key([mod, "control", "shift"], "l", lazy.layout.shrink_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "u", lazy.layout.reset()),
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Select layouts
    Key([mod, "shift"], "t", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "t", lazy.to_layout_index(0), desc="Select columns layout"),
    Key([mod], "m", lazy.to_layout_index(1), desc="Select monadtall layout"),
    Key([mod, "shift"], "m", lazy.to_layout_index(2), desc="Select max layout"),
    Key([mod, "control"], "m", lazy.to_layout_index(3), desc="Select monadwide layout"),
    Key([mod], "Tab", lazy.next_screen()),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    # Key([mod], "Escape", lazy.spawn("pow"), desc="power menu"),
    Key([mod], "Escape", power_menu, desc="power menu"),
    Key(
        [mod],
        "z",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on focused window",
    ),
    Key(
        [mod],
        "f",
        lazy.window.toggle_floating(),
        desc="Toggle floating on focused window",
    ),
    Key([mod], "Tab", lazy.group.next_window(), desc="Cycle through windows"),
    Key(
        [mod, "shift"],
        "Tab",
        lazy.group.prev_window(),
        desc="Cycle backwards through windows",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Rofi
    Key([mod], "space", lazy.spawn("rofi -show drun"), desc="Spawn rofi apps"),
    Key(
        [mod, "control"], "space", lazy.spawn("rofi -show run"), desc="Spawn rofi apps"
    ),
    Key([mod], "w", lazy.spawn("rofi -show window"), desc="Spawn rofi"),
    Key([mod], "n", wifi_menu, desc="Spawn rofi WiFi menu"),
    Key([mod], "r", recorder_menu, desc="Spawn rofi recorder menu"),
    Key([mod], "b", bluetooth_menu, desc="Spawn rofi bluetooth menu"),
    Key([mod, "shift"], "b", lazy.hide_show_bar(), desc="Hide or show bar"),
    # Key([], "XF86AudioRaiseVolume", raise_volume),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("volume up"), desc="Update volume in bar"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("volume down"), desc="Update volume in bar"),
    Key([], "XF86AudioMute", lazy.spawn("volume mute"), desc="Update volume in bar"),
    # Key([], "XF86AudioMute", toggle_mute_audio_output),
    # Key([], "XF86AudioLowerVolume", lower_volume),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightness down")),
    # Key([], "XF86MonBrightnessDown", decrease_brightness),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightness up")),
    # Key([], "XF86MonBrightnessUp", increase_brightness),
    # Key([], "XF86AudioMicMute", toggle_mute_audio_input),
    # ScratchPad keys
    # Key([mod, "shift"], "p", lazy.group["menu"].dropdown_toggle("menu")),
    Key([mod, alt], "p", lazy.spawn("displayselect")),
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),
    # Application chords
    KeyChord([mod], "o", [
        Key([], "b", lazy.spawn("brave")),
        Key([], "q", lazy.spawn("qalculate-gtk")),
        Key([], "v", lazy.spawn("pavucontrol")),
    ]),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            Key(
                [mod, "control"],
                i.name,
                lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                "space",
                lazy.group["scratchpad"].dropdown_toggle("term"),
            ),
            Key(
                [mod, "shift"],
                "a",
                lazy.group["scratchpad"].dropdown_toggle("bitwarden"),
            ),
            Key(
                [mod, "shift"],
                "backspace",
                lazy.group["scratchpad"].dropdown_toggle("menu"),
            ),
            Key(
                [mod, "shift"],
                "p",
                lazy.group["scratchpad"].dropdown_toggle("launcher"),
            ),
        ]
    )

# ScratchPads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "bitwarden", "bitwarden-desktop", x=0.2, y=0.1, height=0.8, width=0.6
            ),
            DropDown(
                "term", terminal, x=0.2, y=0.2, opacity=0.8, height=0.4, width=0.6
            ),
            DropDown(
                "menu",
                "st -e pow --fzf",
                x=0.4,
                y=0.4,
                opacity=0.8,
                height=0.15,
                width=0.15,
                on_focus_lost_hide=True,
            ),
            DropDown(
                "launcher",
                "st -e launcher",
                x=0.2,
                y=0.2,
                opacity=0.8,
                height=0.6,
                width=0.3,
                on_focus_lost_hide=False,
            ),
        ],
    ),
)

config = {
    "margin": 2,
    "single_margin": 2,
    "border_focus": Colours.ELECTRIC_BLUE,
    "border_normal": Colours.GREY,
}

layouts = [
    Columns(**config),
    MonadTall(**config),
    Max(**config),
    MonadWide(**config),
    Floating(**config),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Spiral(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=FONT_TYPE,
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    # Primary screen (e.g., laptop)
    Screen(
        top=top_bar,
        wallpaper=WALLPAPER,
        wallpaper_mode="stretch",
    ),
    # Secondary screen (e.g., external monitor)
    Screen(
        top=top_bar2,
        wallpaper=WALLPAPER,
        wallpaper_mode="stretch",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = Floating(
    border_width=2,
    border_focus=Colours.ELECTRIC_BLUE,
    border_normal=Colours.DARK_BLUE,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "*": InputConfig(left_handed=False, pointer_accel=False),
    "type:keyboard": InputConfig(kb_layout="no", kb_options="caps:escape"),
    "type:pointer": InputConfig(tap=True),
    "type:touchpad": InputConfig(tap=True),
}
# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
