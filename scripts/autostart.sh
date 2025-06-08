#!/bin/sh

# Start dunst notification daemon
dunst &

# Lock screen command
lockscreen="swaylock -i ~/Pictures/Wallpapers/austria.jpg --clock"

# Timings
dim_timeout=60                 # 1 minute of inactivity to dim
lock_timeout=100               # 10 minutes of inactivity to lock

# Screen 
BRIGHTNESS_FILE="/tmp/prev_brightness"
swayidle -w \
    timeout $dim_timeout "brillo -G > $BRIGHTNESS_FILE && brillo -S 10" \
    resume "[ -f $BRIGHTNESS_FILE ] && brillo -S \$(cat $BRIGHTNESS_FILE)" \
    timeout $lock_timeout "~/scripts/lock-then-sleep.sh" \
    resume "[ -f $BRIGHTNESS_FILE ] && brillo -S \$(cat $BRIGHTNESS_FILE)" &

