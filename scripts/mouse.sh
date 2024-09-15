#!/bin/sh

### MOUSE ###

logitech_g_pro_pointer_id=$(xinput | grep 'Logitech G Pro' | grep 'pointer' | sed -n 's/^.*id=\([0-9]*\).*/\1/p')
if [[ -z "$logitech_g_pro_pointer_id" ]]; then
    echo "logitech_ids is empty"
else
    # slow down Logitech G Pro cusor sensitivity
    xinput set-prop "$logitech_g_pro_pointer_id" "Coordinate Transformation Matrix" 0.2 0 0 0 0.2 0 0 0 1 
fi
