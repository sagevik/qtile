#!/bin/sh

### DISPLAY ###

if [ "$1" = "EXTERNAL" ]; then
    xrandr --output DP-3-3 --auto --primary
    xrandr --output eDP-1 --off
    
else
    xrandr --output eDP-1 --auto --primary
    xrandr --output DP-3-3 --off
fi
