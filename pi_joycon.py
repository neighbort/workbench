from evdev import InputDevice, categorize, ecodes, list_devices

# デバイス一覧を取得
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    print(device.path, device.name)
    if 'Joy-Con' in device.name:
        joycon = device
        joycon_name = device.name
        break
print("connceted to ", joycon_name)


print(f"Listening on {joycon.name}")
for event in joycon.read_loop():
    print(event)
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        print(key_event)

