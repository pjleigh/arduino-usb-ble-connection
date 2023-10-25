import asyncio
import signal
from bleak import BleakClient, BleakScanner

# variables
YOUR_DEVICE_NAME = "NanoRP2040" # name of ble device
CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb" # name of notification characteristic

# function to be called whenever data streams
def callback(sender: int, data: bytearray):
    print(f"Received data: {int.from_bytes(data, byteorder='little')}")

async def main():

    # finds all ble addresses, searches for one that matches device name above
    devices = await BleakScanner.discover()
    target_device = None

    for device in devices:
        if device.name == YOUR_DEVICE_NAME:
            print("Found target device: ", device.name)
            target_device = device
            break

    # returns if cannot find device
    if not target_device:
        print(f"Device {YOUR_DEVICE_NAME} not found!")
        return
    
    async with BleakClient(target_device.address, timeout=60) as client:

        # gets data over ble notification
        await client.start_notify(CHARACTERISTIC_UUID, callback)

        # sets up exception handling
        stop_event = asyncio.Event()

        def signal_handler(sig, frame):
            stop_event.set()

        signal.signal(signal.SIGINT, signal_handler)

        # ensures proper exit when stop event occurs
        try:
            while not stop_event.is_set():
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            pass

        # ends ble notifications
        await client.stop_notify(CHARACTERISTIC_UUID)
        print("Stopped notifications.")
        return

if __name__ == "__main__":
    asyncio.run(main())
