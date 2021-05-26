import  os
import  re
import socket
import subprocess
import psutil
from typing import List  # noqa: F401

from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "j", lazy.layout.shrink()),
    Key([mod, "control"], "k", lazy.layout.grow()),
    Key([mod, "control"], "n", lazy.layout.normalize()),
    Key([mod, "control"], "m", lazy.layout.maximize()),
    Key([mod, "control"], "space", lazy.layout.flip()),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "#e3eaee",
                "border_normal": "#30586f",
                }

layouts = [
    # layout.Columns(border_focus_stack='#d75f5f'),
    layout.MonadTall(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Floating(**layout_theme)
]


colors = [["#e3eaee", "#e3eaee"], # 0 panel background                        ->  Gray
          ["#9ab2c0", "#9ab2c0"], # 1 background for current screen tab
          ["#30586f", "#30586f"], # 2 font color for group names
          ["#ff2800", "#ff2800"], # 3 border line color for current tab
          ["#3c6e8a", "#3c6e8a"], # 4 border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"]] # 5 window name

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2],
    foreground=colors[0],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    background = colors[2],
                    foreground = colors[2],
                    padding = 2,
                ),
                widget.CurrentLayoutIcon(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 2,
                ),
                widget.CurrentLayout(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 2,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.GroupBox(
                    background = colors[0],
                    foreground = colors[2],
                    padding = 2,
                    margin_y = 3,
                    margin_x = 3,
                    padding_y = 5,
                    padding_x = 3,
                    borderwith = 3,
                    active = colors[3],
                    inactive = colors[4],
                    block_highlight_text_color = colors[2],
                    center_aligned = True,
                    disable_drag = True,
                    hide_unused = True,
                    rounded = True,
                    highlight_method = "line",
                    highlight_color = colors[0],
                    this_current_screen_border = colors[5],
                    this_current_border = colors[4],
                    other_current_screen_border = colors[5],
                    other_current_border = colors[4],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Prompt(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.WindowName(
                    background = colors[0],
                    foreground = colors[2],
                    padding = 2,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Net(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 2,
                    interface = "enp39s0",
                ),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.CheckUpdates(
                    background = colors[0],
                    foreground = colors[2],
                    padding = 4,
                    custom_command = 'paru -Sy',
                    execute = 'paru -Syu',
                    colour_have_updates = colors[3],
                    colour_no_updates = colors[2],
                    display_format = 'Updates: {updates}',
                    no_update_string = 'No Updates',
                    restart_indicator = 'Restart Required',
                    distro = 'Arch',
                    update_interval = 3600,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Volume(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 4,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.KeyboardLayout(
                    background = colors[0],
                    foreground = colors[2],
                    padding = 4,
                    configured_keyboards = ['us', 'ir'],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Systray(
                    background = colors[0],
                    padding = 2,
                    icon_size = 14,
                    ),
                widget.Sep(
                    background = colors[0],
                    foreground = colors[0],
                    padding = 2,
                ),
            ],
            opacity = 1.0,
            size = 24,
        ),
        bottom=bar.Bar(
            [
                widget.Sep(
                    background = colors[2],
                    foreground = colors[2],
                    padding = 2,
                ),
                widget.Wallpaper(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 4,
                    label = 'Wallpaper',
                    directory = '~/Pictures/gnome',
                    random_selection = True,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.CapsNumLockIndicator(
                    background = colors[0],
                    foreground = colors[2],
                    padding = 2,
                    update_interval = 1.0,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.TaskList(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 4,
                    border = colors[4],
                    highlight_method = colors[3],
                    icon_size = 14,
                    rounded = True,
                    urgent_alert_method = 'text',   # text or border
                    urgent_border = colors[4],
                    ),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Memory(
                    background = colors[0],
                    foreground = colors[2],
                    padding = 4,
                    mouse_callbacks = {terminal + "-e free -h"},
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[2],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.CPU(
                    background = colors[2],
                    foreground = colors[0],
                    mouse_callbacks = {terminal + "-e top"},
                    padding = 4,
                    update_interval = 1.0,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[2],
                    foreground = colors[0],
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Clipboard(
                    background = colors[2],
                    foreground = colors[0],
                    padding = 2,
                ),
            ],
            size=24,
        )
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='xfce4-appfinder'),  # xfce4-appfinder
    Match(wm_class='Steam'),  # Steam
    Match(wm_class='steam-app-*'),  # Steam
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
