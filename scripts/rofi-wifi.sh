#!/usr/bin/env bash

config_dir="$XDG_CONFIG_HOME/rofi"

search=''
shut_lock=''
open_lock=''
wifi_enable='󰖩'
wifi_disable='󰖪'

notify-send "Getting list of available Wi-Fi networks..."
wifi_list=$(nmcli --fields "SECURITY,SSID" device wifi list | sed 1d | sed 's/  */ /g' | sed -E "s/WPA*.?\S/$shut_lock /g" | sed "s/^--/$open_lock /g" | sed "s/$shut_lock  $shut_lock/$shut_lock/g" | sed "/--/d")

connected=$(nmcli -fields WIFI g)
if [[ "$connected" =~ "enabled" ]]; then
	toggle="$wifi_disable  Disable Wi-Fi"
elif [[ "$connected" =~ "disabled" ]]; then
	toggle="$wifi_enable  Enable Wi-Fi"
fi

selected_network=$(echo -e "$toggle\n$wifi_list" | uniq -u | rofi -dmenu -i -selected-row 1 -p "Wi-Fi SSID: " -theme ${config_dir}/wi-fi )
read -r chosen_id <<< "${selected_network:3}"

if [ "$selected_network" = "" ]; then
	exit
elif [ "$selected_network" = "$wifi_enable  Enable Wi-Fi" ]; then
	nmcli radio wifi on
elif [ "$selected_network" = "$wifi_disable  Disable Wi-Fi" ]; then
	nmcli radio wifi off
else
  success_message="You are now connected to the Wi-Fi network \"$chosen_id\"."
	saved_connections=$(nmcli -g NAME connection)
	if [[ $(echo "$saved_connections" | grep -w "$chosen_id") = "$chosen_id" ]]; then
		nmcli connection up id "$chosen_id" | grep "successfully" && notify-send "Connection Established" "$success_message"
	else
		if [[ "$selected_network" =~ $shut_lock ]]; then
			wifi_password=$(rofi -dmenu -p "Password: " )
		fi
		nmcli device wifi connect "$chosen_id" password "$wifi_password" | grep "successfully" && notify-send "Connection Established" "$success_message"
    fi
fi
