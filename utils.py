# Importing dbus
import dbus
from os import system

# Creating bus
bus = dbus.SystemBus()

# Do you want debuging info ?
debug = False

def power_on(UE_BOOM_MAC, YOUR_BT_MAC):

	# Checking i you're connecting to the device
	if(not is_connected(UE_BOOM_MAC)):
		connect_device(UE_BOOM_MAC)

	# Parsing your MAC to create the value array
	value = [eval(f"0x{x}") for x in YOUR_BT_MAC.split(":")]
	value.append(0x01)

	# Setting path
	device_path = MAC_to_device_path(UE_BOOM_MAC)
	service_path = "/service0001/char0002"
	
	# Write the value to the GATT characteristic
	try:
		char_obj = bus.get_object('org.bluez', device_path + service_path)
		char_iface = dbus.Interface(char_obj, 'org.bluez.GattCharacteristic1')
		char_iface.WriteValue(value, {})
	except dbus.exceptions.DBusException as e:
		print("[!] UE Boom arleady on.")
		return

	print("UE Boom switched on.")

	return

def power_off(UE_BOOM_MAC, YOUR_BT_MAC):
	# Connecting to the device with bluetoothctl otherwise this will produce an error (idk why)
	connect_device(UE_BOOM_MAC, for_off=True)

	# Parsing your MAC to create the value array
	value = [eval(f"0x{x}") for x in YOUR_BT_MAC.split(":")]
	value.append(0x02)

	# Setting path
	device_path = MAC_to_device_path(UE_BOOM_MAC)
	service_path = "/service0001/char0002"
	
	# Write the value to the GATT characteristic
	try:
		char_obj = bus.get_object('org.bluez', device_path + service_path)
		char_iface = dbus.Interface(char_obj, 'org.bluez.GattCharacteristic1')
		char_iface.WriteValue(value, {})
	except dbus.exceptions.DBusException as e:
		print("[!] This error happened when you were arleady connected to the Boom.")
		print(e)
		return

	print("UE Boom switched off.")
	return

def get_battery(UE_BOOM_MAC):

	# Checking i you're connecting to the device
	if(not is_connected(UE_BOOM_MAC)):
		connect_device(UE_BOOM_MAC)

	# Setting service identification
	device_path = MAC_to_device_path(UE_BOOM_MAC)
	service_path = "/service0001/char0013"

	# Reading the GATT characteristic value
	device_obj = bus.get_object('org.bluez', device_path)
	device_props = dbus.Interface(device_obj, 'org.freedesktop.DBus.Properties')
	characteristic_obj = bus.get_object('org.bluez', device_path + service_path)
	characteristic_props = dbus.Interface(characteristic_obj, 'org.freedesktop.DBus.Properties')
	
	# Getting and parsing value
	value = characteristic_props.Get('org.bluez.GattCharacteristic1', 'Value')
	value = bytearray(value)
	value = ' '.join(format(b, '02x') for b in value)
	value = eval(f"0x{value}")

	# Returing decimal % value
	return value

def is_connected(UE_BOOM_MAC):
	if debug:
		print("(i) Checking if you're connected to the device ...")

	device_path = MAC_to_device_path(UE_BOOM_MAC)
	device_obj = bus.get_object('org.bluez', device_path)
	device_props = dbus.Interface(device_obj, 'org.freedesktop.DBus.Properties')

	connected = device_props.Get('org.bluez.Device1', 'Connected')

	if connected:
		if debug:
			print("(i) Yes you were.")
	else:
		if debug:
			print("(i) No, you weren't.")

	return connected

def connect_device(UE_BOOM_MAC, for_off=False):
	if for_off:
		system(f'/bin/bash -c "bluetoothctl -- connect {UE_BOOM_MAC} &> /dev/null"')
		return

	if debug:
		print("(i) Connecting to the device ...")

	device_path = MAC_to_device_path(UE_BOOM_MAC)
	device_obj = bus.get_object('org.bluez', device_path)
	device_iface = dbus.Interface(device_obj, 'org.bluez.Device1')

	try:
		device_iface.Connect()
		while True:
			connected = device_iface.Connected
			if connected:
				if debug: 
					print("(i) Successfuly connected.")
				break
	except dbus.exceptions.DBusException as e:
		print(f"[!] Failed to connect : {e}")

def is_bluetooth_enabled():
	adapter_obj = bus.get_object('org.bluez', '/org/bluez/hci0')
	adapter_props = dbus.Interface(adapter_obj, 'org.freedesktop.DBus.Properties')

	powered = adapter_props.Get('org.bluez.Adapter1', 'Powered')
	
	return powered

def MAC_to_device_path(UE_BOOM_MAC):
	UE_BOOM_MAC = UE_BOOM_MAC.replace(":", "_")
	return f"/org/bluez/hci0/dev_{UE_BOOM_MAC}"