from libqtile import qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating


from settings.top_bar import top_bar
from settings.commands import (
    Brightness,
    Microphone,
    power_menu,
    wifi_menu,
    bluetooth_menu,
    autostart,
    setup_mouse,
    setup_display,
)
from settings.constants import Colours, WALLPAPER_HONG_KONG, FONT_TYPE

SCRIPTS_PATH = "~/.config/qtile/scripts"

mod = "mod4"
terminal = "alacritty"


@hook.subscribe.startup_once
def on_startup():
    autostart()
    setup_display()
    setup_mouse()


@hook.subscribe.screen_change
def on_screenshange():
    setup_display()
    setup_mouse()


keys = [
    # see: https://docs.qtile.org/en/latest/manual/config/lazy.html
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.reset()),
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "d", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "Tab", lazy.next_screen()),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "Escape", power_menu, desc="power menu"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn rofi apps"),
    Key([mod], "w", lazy.spawn("rofi -show window"), desc="Spawn rofi"),
    Key([mod], "n", wifi_menu, desc="Spawn rofi WiFi menu"),
    Key([mod], "b", bluetooth_menu, desc="Spawn rofi bluetooth menu"),
    # messaging key
    Key([], "XF86Messenger", lazy.spawn("kotatogram-desktop")),
    # favourites key
    Key([], "XF86Favorites", lazy.spawn("firefox")),
    # bluetooth/phone keys
    Key([], "XF86Go", lazy.spawn("rfkill unblock bluetooth")),
    Key([], "Cancel", lazy.spawn("rfkill block bluetooth")),
    # volume
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+")),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-")),
    Key([], "XF86MonBrightnessDown", lazy.spawn(Brightness.decrease_brightness_cmd())),
    Key([], "XF86MonBrightnessUp", lazy.spawn(Brightness.increase_brightness_cmd())),
    # mute microphone
    Key([], "XF86AudioMicMute", lazy.spawn(Microphone.toggle_microphone_mute_cmd())),
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
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

config = {
    "margin": 10,
    "single_margin": 10,
    "border_focus": Colours.ELECTRIC_BLUE,
    "border_normal": Colours.GREY,
}

layouts = [
    MonadTall(**config),
    Max(**config),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
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

main_screen = Screen(
    top=top_bar,
    wallpaper=WALLPAPER_HONG_KONG,
    wallpaper_mode="stretch",
)

screens = [main_screen]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

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
