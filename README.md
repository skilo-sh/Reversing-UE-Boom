<img src="https://yt3.ggpht.com/-pNGL_fZt-wo/AAAAAAAAAAI/AAAAAAAAAAA/86MBTnIqSZQ/s900-c-k-no-mo-rj-c0xffffff/photo.jpg" alt="Logo UE" style="width: 100px; height: 100px;" />

# Reversing UE Boom speaker

## Description

This repository provides code and informations for controling the Bluetooth connection of a UE Boom speaker.<br>
The goal of this project is to control the speaker remotely, enabling functions such as power on/off and battery status retrieval.<br>
The reverse engineering process involves analyzing GATT requests, decoding the communication protocol, and interacting with the speaker using bluetoothctl and D-Bus scripting.<br>

## Reverse Engineering Process

### Wireshark
After recording the communications from my phone to my speaker in a log file, I was able to deduce that : 
- The application uses GATT
- The value for switching on the speaker is MAC+01, where MAC is the MAC address of a device already paired with the speaker.
- The same applies to turning the speaker off, but it's MAC+02.

All I needed to know was which attribute was used for the ATT write request, which is where the reverse of the Android application came in handy.

### Reversing android app
In the "com/logitech/ue/centurion/legacy/ble/BLECommand.java" file of the App, we can see all the GATT attributes used to communicate with the speaker.<br>
I had listed them in the "" file, this allowed me to gather the information needed to create the python script. 

## Interaction with Speaker

### PoC
Just for a PoC you can use bluetoothctl (don't use gatttol, that's depracted).<br>
*Before any commmand, first connect to the speaker (even if it is off, you still can connect to BLE device)*

```
# Turning on 
bluetoothctl
menu gatt
select-attribute c6d6dc0d-07f5-47ef-9b59-630622b01fd3
write "140 122 61 195 63 24 1" # Dont' ask me why u should convert in decimal
```
```
# Turning off
bluetoothctl
menu gatt
select-attribute c6d6dc0d-07f5-47ef-9b59-630622b01fd3
write "140 122 61 195 63 24 2"
```
```
# Get battery
bluetoothctl
menu gatt
select-attribute 00002a19-0000-1000-8000-00805f9b34fb
read
```

## Scripting
Now, for scripting, don't use bluetoothctl, prefer the D-bus API ( I have choose the python one ).<br>
You can use my script by following instructions in main.py.<br><br>
The following functions are available:
```PY
power_on(UE_BOOM_MAC, YOUR_BT_MAC)
power_off(UE_BOOM_MAC, YOUR_BT_MAC)
get_battery(UE_BOOM_MAC)
is_connected(UE_BOOM_MAC)
connect_device(UE_BOOM_MAC)
is_bluetooth_enabled()
```

## Notes
    This project uses bluetoothctl for interaction due to its compatibility with modern Bluetooth devices.
    D-Bus scripting is preferred over other methods due to improved stability and parsing capabilities compared to direct bluetoothctl output.

## Disclaimer
  This repository is for educational and research purposes only. Reverse engineering Bluetooth devices and their protocols may involve legal and ethical considerations. Please ensure you have the necessary permissions before attempting any reverse engineering activities.
