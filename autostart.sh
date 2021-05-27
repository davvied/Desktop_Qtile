#!/usr/bin/env bash 

xfsettingsd &
firewall-applet &
picom &
# nitrogen --restore &
# volumeicon &
nm-applet &
numlockx &
nvidia-settings --config ~/.nvidia-settings-rc -l &