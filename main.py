from utils import power_on, power_off, get_battery, is_bluetooth_enabled
from time import sleep

def main():
	
	UE_BOOM_MAC = "EC:81:93:59:71:AE"
	YOUR_BT_MAC = "2C:33:58:43:D7:93"# Or can be any mac that was paired with UE Boom

	# Checking if bluetooth is enabled
	if(not is_bluetooth_enabled()):
		print("Switch on bluetooth please.")
		exit(1)

	# Switch on the speaker
	power_on(UE_BOOM_MAC, YOUR_BT_MAC)

	# Get the battery level
	battery_level = get_battery(UE_BOOM_MAC)
	print(f"Battery : {battery_level}%")

	# Waiting 10 seconds
	sleep(10)
	print("Waiting 10 seconds before switching off ...")
	print("(doing to quickly result in a bug)")
	
	# Switch off the speaker
	power_off(UE_BOOM_MAC, YOUR_BT_MAC)

	# Get the battery level - can be done even if the speaker is off
	battery_level = get_battery(UE_BOOM_MAC)
	print(f"Battery : {battery_level}%")

if __name__ == '__main__':
	main()