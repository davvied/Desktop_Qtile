#!/usr/bin/env bash 

xfsettingsd &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
# gnome-keyring-daemon &
firewall-applet &
picom &
# volumeicon &
nm-applet &
numlockx &
nvidia-settings --config ~/.nvidia-settings-rc -l &
wal -q -R &
# variety &
