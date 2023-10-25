# arduino-usb-ble-connection

Simple USB host and device, and BLE client and server for sending data from an arduino or similar microcontroller to a python script.
- Reads in from pin A0 and sends it over USB or BLE. Receives and unpacks on the python side with some additional wrapping for exception handling.
- Includes some setup scripts and scanners to help find addresses/ports to set variables for connection.
