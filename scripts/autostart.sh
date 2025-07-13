#!/bin/sh

# Start dunst notification daemon
xmodmap $HOME/.Xmodmap &
dunst &
blueman-applet &
nm-applet &
archupdate -b &

# Lock screen command
lockscreen="slock"
# lockscreen="swaylock -i ~/Pictures/Wallpapers/austria.jpg --clock"

# Timings
dim_timeout=120  # 1 minute of inactivity to dim
lock_timeout=300 # 5 minutes of inactivity to lock

# Screen
# BRIGHTNESS_FILE="/tmp/prev_brightness"
# swayidle -w \
# 	timeout $dim_timeout "brillo -G > $BRIGHTNESS_FILE && brillo -S 10" \
# 	resume "[ -f $BRIGHTNESS_FILE ] && brillo -S \$(cat $BRIGHTNESS_FILE)" \
# 	timeout $lock_timeout "$HOME/.config/qtile/scripts/sleep.sh" \
# 	resume "[ -f $BRIGHTNESS_FILE ] && brillo -S \$(cat $BRIGHTNESS_FILE)" &
