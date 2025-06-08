#!/bin/sh

swaylock -i ~/Pictures/Wallpapers/austria.jpg --clock &
sleep 10 # Now suspend (after swaylock has released the inhibitor)
systemctl suspend
