import  os, json
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
WebBrowser = "firefox"

# Switch between windows
keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

# Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "space", lazy.layout.flip(), desc="Change stack side"),

# Change windows size
    Key([mod, "control"], "j", lazy.layout.shrink()),
    Key([mod, "control"], "k", lazy.layout.grow()),
    Key([mod, "control"], "n", lazy.layout.normalize()),
    Key([mod, "control"], "m", lazy.layout.maximize()),

# Switch monitor focus
    Key([mod], "period", lazy.to_screen(0), desc='Keyboard focus to monitor 1'),
    Key([mod], "comma", lazy.to_screen(1), desc='Keyboard focus to monitor 2'),
    # Key([mod], "r", lazy.to_screen(2), desc='Keyboard focus to monitor 3'),
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),

# qtile controls
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

# Media keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 2%+ -q"), desc="Rise Volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 2%- -q"), desc="Lower Volume"),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle -q"), desc="Lower Volume"),
    Key(["control", "shift"], "Escape", lazy.spawn("gnome-system-monitor")),

groups = [Group(i) for i in "123456789"],

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

def pywal_colors(name):
    home = os.path.expanduser('~')
    try:
        os.chdir(home + "/.cache/wal/")
        colors_list = json.load(open("colors.json"))
        colors_dic = colors_list["colors"]
        return colors_dic[name]
    except:
        colors_dic = {
            "color0": "#30586f",    # 0 background for current screen tab       ->  Gray-white
            "color2": "#9ab2c0",    # 2 panel foreground                        ->  white-gray
            "color4": "#4f76c7",    # 4 window name                             ->  Light-Purple
            "color5": "#3c6e8a",    # 5 border line color for 'other tabs' and color for 'odd widgets'        ->  Dark-Blue
            "color6": "#9ab2c0",    # 6 font color for group names              ->  Dark-Blue
            "color7": "#ff2800",    # 7 border line color for current tab       ->  Orange
        }
        return colors_dic[name]

# def window_to_prev_group(qtile):
#     if qtile.currentWindow is not None:
#         i = qtile.groups.index(qtile.currentGroup)
#         qtile.currentWindow.togroup(qtile.groups[i - 1].name)

# def window_to_next_group(qtile):
#     if qtile.currentWindow is not None:
#         i = qtile.groups.index(qtile.currentGroup)
#         qtile.currentWindow.togroup(qtile.groups[i + 1].name)

# def window_to_previous_screen(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     if i != 0:
#         group = qtile.screens[i - 1].group.name
#         qtile.current_window.togroup(group)

# def window_to_next_screen(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     if i + 1 != len(qtile.screens):
#         group = qtile.screens[i + 1].group.name
#         qtile.current_window.togroup(group)

# def switch_screens(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     group = qtile.screens[i - 1].group
#     qtile.current_screen.set_group(group)

widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background = pywal_colors("color1"),
    foreground = pywal_colors("color0"),
)

screens = [

    Screen(

        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color2"),
                    padding = 2,
                ),
                widget.CurrentLayoutIcon(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 2,
                ),
                widget.CurrentLayout(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 2,
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.GroupBox(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 2,
                    margin_y = 3,
                    margin_x = 3,
                    padding_y = 5,
                    padding_x = 3,
                    borderwith = 3,
                    active = pywal_colors("color7"),
                    inactive = pywal_colors("color1"),
                    block_highlight_text_color = pywal_colors("color0"),
                    center_aligned = True,
                    disable_drag = True,
                    hide_unused = True,
                    rounded = True,
                    highlight_method = "line",
                    highlight_color = pywal_colors("color5"),
                    this_current_screen_border = pywal_colors("color7"),
                    this_current_border = pywal_colors("color6"),
                    other_current_screen_border = pywal_colors("color5"),
                    other_current_border = pywal_colors("color4"),
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Prompt(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color0"),
                    padding = 0,
                    ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.WindowName(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color0"),
                    padding = 2,
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Net(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                    interface = "enp39s0",
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.CheckUpdates(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                    colour_have_updates = pywal_colors("color7"),
                    colour_no_updates = pywal_colors("color1"),
                    display_format = 'Updates: {updates}',
                    no_update_string = 'No Updates',
                    restart_indicator = 'Restart Required',
                    distro = 'Arch',
                    update_interval = 1800,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e paru -Syu')},
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Volume(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.KeyboardLayout(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                    configured_keyboards = ['us', 'ir'],
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                # widget.KhalCalendar(
                #     background = colors[2],
                #     foreground = colors[0],
                #     padding = 4,
                #     reminder_color = colors[3],
                #     remindertime = 10,
                #     lookahead = 7,
                #     update_interval = 60,
                #     mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + 'khal --color interactive')}
                # ),
                # widget.TextBox(
                #     text = '',
                #     background = pywal_colors("color6"),
                #     foreground = pywal_colors("color1"),
                #     padding = 0,
                #     fontsize = 24,
                #     ),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Systray(
                    background = pywal_colors("color6"),
                    padding = 2,
                    icon_size = 14,
                    ),
                widget.Sep(
                    foreground = pywal_colors("color6"),
                    background = pywal_colors("color6"),
                    padding = 2,
                ),
            ],
            opacity = 1.0,
            size = 24,
        ),

        bottom=bar.Bar(
            [
                widget.Sep(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color2"),
                    padding = 2,
                ),
                # widget.Wallpaper(
                #     # background = colors[2],
                #     # foreground = colors[0],
                #     background = pywal_colors("color1"),
                #     foreground = pywal_colors("color3"),
                #     padding = 4,
                #     label = 'Wallpaper',
                #     directory = '~/Pictures/gnome',
                #     random_selection = True,
                # ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.CapsNumLockIndicator(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                    update_interval = 1.0,
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.TaskList(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                    border = pywal_colors("color5"),
                    highlight_method = pywal_colors("color3"),
                    icon_size = 14,
                    rounded = True,
                    urgent_alert_method = 'text',   # text or border
                    urgent_border = pywal_colors("color7"),
                    ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Memory(
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color0"),
                    padding = 4,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("gnome-system-monitor")},# (terminal + ' -e top')},
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color6"),
                    foreground = pywal_colors("color2"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.CPU(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e top')},
                    padding = 4,
                    update_interval = 1.0,
                ),
                widget.TextBox(
                    text = '',
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color6"),
                    padding = 0,
                    fontsize = 24,
                    ),
                widget.Clipboard(
                    background = pywal_colors("color2"),
                    foreground = pywal_colors("color0"),
                    padding = 2,
                ),
            ],
            size=24,
        )
    ),

    Screen(

        top=bar.Bar(
            [
                widget.CPU(
                background = pywal_colors("color1"),
                foreground = pywal_colors("color0"),
                mouse_callbacks = {terminal + "-e top"},
                padding = 4,
                update_interval = 1.0,
                ),
            ],
            size = 24,
            ),
        ),
]

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
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='pinentry-gtk-2'),  # Steam
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.restart
def restart():
    home = os.path.expanduser('~')
    try:
        subprocess.call([home + '/.config/qtile/startup_rep.sh'])
    except:
        None

# @hook.subscribe.startup
# def startup():
#     home = os.path.expanduser('~')
#     subprocess.call([home + '/.config/qtile/startup_rep.sh'])

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    try:
        subprocess.call([home + '/.config/qtile/autostart.sh'])
    except:
        None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
