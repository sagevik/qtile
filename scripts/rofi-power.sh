#!/usr/bin/env bash

config_dir="$XDG_CONFIG_HOME/rofi"

uptime="`uptime -p | sed -e 's/up //g'`"
host="x1"

shutdown=''
reboot=''
lock=''
suspend='󰏤'
logout='󰗽'
yes=''
no=''

rofi_cmd() {
	rofi -dmenu -p "Uptime: $uptime" -mesg "Uptime: $uptime" -theme ${config_dir}/power.rasi
}

confirm_cmd() {
	rofi -theme ${config_dir}/power.rasi -theme-str 'listview {columns: 2; lines: 1;}' -dmenu -p 'Confirmation' -mesg 'Confirm?' 
}

confirm_exit() {
	echo -e "$yes\n$no" | confirm_cmd
}

run_rofi_with_vars() {
	echo -e "$lock\n$suspend\n$logout\n$reboot\n$shutdown" | rofi_cmd
}

run_cmd() {
	selected="$(confirm_exit)"
	if [[ "$selected" == "$yes" ]]; then
		if [[ $1 == '--shutdown' ]]; then
			systemctl poweroff
		elif [[ $1 == '--reboot' ]]; then
			systemctl reboot
		elif [[ $1 == '--suspend' ]]; then
			mpc -q pause
			amixer set Master mute
			systemctl suspend
		elif [[ $1 == '--logout' ]]; then
      qtile-logoff
		fi
	else
		exit 0
	fi
}

selected="$(run_rofi_with_vars)"
case ${selected} in
    $shutdown)
		run_cmd --shutdown
        ;;
    $reboot)
		run_cmd --reboot
        ;;
    $lock)
    dm-tool lock
        ;;
    $suspend)
		run_cmd --suspend
        ;;
    $logout)
		run_cmd --logout
        ;;
esac
