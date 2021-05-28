#!/usr/bin/env bash 

xfsettingsd &
# /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
firewall-applet &
picom &
# nitrogen --restore &
# volumeicon &
# gnome-keyring-daemon &
nm-applet &
numlockx &
nvidia-settings --config ~/.nvidia-settings-rc -l &
variety &
