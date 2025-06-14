#!/bin/sh

if pactl list sink-inputs | grep -q 'state: RUNNING'; then
	exit 0 # Audio is playing — do not lock
else
	swaylock -i ~/Pictures/Wallpapers/austria.jpg --clock &
	sleep 10
	systemctl suspend
fi
