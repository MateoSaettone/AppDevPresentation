import asyncio
from bleak import BleakClient

# Replace this with your Polar H10 MAC address
mac_address = "EB:D9:AB:99:89:8F"

# UUID for the Heart Rate Measurement characteristic
heart_rate_char_uuid = "00002a37-0000-1000-8000-00805f9b34fb"

async def run():
    async with BleakClient(mac_address) as client:
        print(f"Connected: {client.is_connected}")
        
        # Function to handle heart rate notifications
        def handle_heart_rate(sender, data):
            # Parse heart rate data according to the Bluetooth GATT specification
            heart_rate = data[1]
            print(f"Heart Rate: {heart_rate} BPM")

        # Start notifications on the heart rate characteristic
        await client.start_notify(heart_rate_char_uuid, handle_heart_rate)
        
        print("Receiving heart rate data... Press Ctrl+C to exit")
        
        # Keep the connection open to receive data
        while True:
            await asyncio.sleep(1)

# Run the asyncio event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
