# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"                             # My terminal of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "r",
             # lazy.spawn("dmenu_run -p 'Run: '"),
             lazy.spawn("rofi -show drun -config ~/.config/rofi/themes/slate.rasi -display-drun \"Run: \" -drun-display-format \"{name}\""),
             # lazy.spawn("rofi -combi-modi window,drun -show combi -modi combi -config ~/.config/rofi/themes/slate.rasi -display-drun \"Run: \" -drun-display-format \"{name}\""),
             desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "c",
             lazy.spawn("xfce4-power-manager"),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "x",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("thunar"),
             desc='file manager'
             ),
         Key([mod, "shift"], "w",
             lazy.spawn("qutebrowser"),
             desc='web browser'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             )
]

group_names = [("1", {'layout': 'monadtall'}),
               ("2", {'layout': 'monadtall'}),
               ("3", {'layout': 'monadtall'}),
               ("4", {'layout': 'monadtall'}),
               ("5", {'layout': 'monadtall'}),
               ("6", {'layout': 'monadtall'}),
               ("7", {'layout': 'monadtall'}),
               ("8", {'layout': 'monadtall'}),
               ("9", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {"border_width": 2,
                "margin": 20,
                "border_focus": "88c0d0",
                "border_normal": "3b4252"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

colors = [["#2e3440", "#2e3440"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#4c566a", "#4c566a"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#88c0d0", "#88c0d0"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Roboto Bold",
    fontsize = 12,
    padding = 2,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
             widget.Sep(
                       linewidth = 0,
                       padding = 1,
                       foreground = colors[2],
                       background = colors[4]
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[4]
                       ),
              widget.GroupBox(
                       font = "Roboto Bold",
                       fontsize = 13,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[7],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[4],
                       highlight_method = "line",
                       this_current_screen_border = colors[7],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[4]
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[4],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 45
                       ),
              # widget.Sep(
              #         linewidth = 0,
              #         padding = 40,
              #         foreground = colors[2],
              #         background = colors[0]
              #         ),
                widget.Spacer(),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[0],
                       padding = 0,
                       fontsize = 45
                       ),
                widget.TextBox(
                    text='',
                    fontsize='34',
                    padding=0,
                    background=colors[4],
                    foreground=colors[0],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=colors[4]
                ),
                widget.TextBox(
                    text='  ',
                    font="FontAwesome",
                    fontsize='14',
                    padding=0,
                    background=colors[4],
                    foreground=colors[2],
                ),
                widget.Clock(
                    font="Roboto bold",
                    foreground=colors[2],
                    background=colors[4],
                    fontsize=14,
                    format = "%A, %B %d - %H:%M "
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=colors[4]
                ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[0],
                       padding = 0,
                       fontsize = 45
                       ),
                widget.Spacer(),
              # widget.Systray(
              #          background = colors[0],
              #          padding = 5
              #          ),
              # widget.Sep(
              #          linewidth = 0,
              #          padding = 6,
              #          foreground = colors[0],
              #          background = colors[0]
              #          ),
              widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 45
                       ),
              widget.TextBox(
                       text = " 🖬",
                       foreground = colors[2],
                       background = colors[4],
                       padding = 0,
                       fontsize = 14
                       ),
              widget.Memory(
                       foreground = colors[2],
                       background = colors[4],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       padding = 5
                       ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=colors[4]
                ),
                widget.TextBox(
                    text=' =',
                    font="FontAwesome",
                    fontsize='18',
                    padding=0,
                    background=colors[4],
                    mouse_callbacks={'Button3': lambda: qtile.cmd_spawn("pavucontrol")},
                    foreground=colors[2],
                ),
                widget.Volume(
                    background=colors[4],
                    foreground="#ffffff",
                    font="Roboto Bold",
                    fontsize=14,
                    mouse_callbacks={'Button3': lambda: qtile.cmd_spawn("pavucontrol")},
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=colors[4]
                ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[4],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 7,
                       foreground = colors[2],
                       background = colors[4]
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, margin=[4,2,0,6], size=23)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, margin=[4,2,0,6], size=23)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, margin=[4,2,0,6], size=23))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
