#!/usr/bin/env bash 

festival --tts $HOME/.config/qtile/welcome_msg &
lxsession &
picom &
nitrogen --restore &
/usr/bin/emacs --daemon &
nm-applet &
dunst &
lxqt-policykit-agent &
xfce4-power-manager &
# flameshot &