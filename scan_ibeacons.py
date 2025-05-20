from bluepy.btle import Scanner

def parse_ibeacon(data):
    try:
        raw = bytes.fromhex(data)
        if raw[0:2] == b'\x4c\x00' and raw[2] == 0x02 and raw[3] == 0x15:
            uuid = raw[4:20].hex()
            major = int.from_bytes(raw[20:22], 'big')
            minor = int.from_bytes(raw[22:24], 'big')
            tx_power = int.from_bytes(raw[24:25], 'big', signed=True)
            return uuid, major, minor, tx_power
    except Exception:
        pass
    return None

scanner = Scanner()
print("A procurar iBeacons...")
devices = scanner.scan(10.0)

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if desc == "Manufacturer" and value:
            parsed = parse_ibeacon(value)
            if parsed:
                uuid, major, minor, tx_power = parsed
                print(f"\n iBeacon encontrado:")
                print(f"  MAC     : {dev.addr}")
                print(f"  UUID    : {uuid}")
                print(f"  Major   : {major}")
                print(f"  Minor   : {minor}")
                print(f"  TX Power: {tx_power} dB")
                print(f"  RSSI    : {dev.rssi} dB")