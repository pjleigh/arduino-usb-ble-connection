import serial
import serial.tools.list_ports
import sys
import signal

# variables
mapping_factor = 255 # b/c ADC range 0-1023 mapped to byte range 0-255 before sending
baudrate = 9600 # serial communication rate 
checkdescription = "Arduino" # description to match when searching serial ports

# create a function to handle Ctrl+C and other exceptions
def signal_handler(sig, frame):
    global ser
    print("Signal received. Exiting gracefully...")
    
    try:
        ser.close()  # Attempt to close the serial port
    except Exception as e:
        print(f"Error while closing the serial port: {e}")

    sys.exit(0)

# reads 1 serial byte, converts 0-255 to 0-1 to voltage reading to current
def read_data():
    data = ser.read(1)
    return (list(data)[0])

# finds all ble addresses, searches for one that matches "Arduino" in description
def connect_arduino():
    # find the Arduino's port dynamically
    arduino_port = None
    ports = list(serial.tools.list_ports.comports())

    for port, desc, hwid in ports:
        if checkdescription in desc:  # adjust the keyword as needed
            print(f"Arduino found at port: {port}. connecting...")
            arduino_port = port

    return arduino_port

def main():

    # register the signal handler for Ctrl+C and other exceptions
    signal.signal(signal.SIGINT, signal_handler)

    arduino_port = connect_arduino()

    ser = serial.Serial(arduino_port, baudrate, timeout=1)
    print("Signal reading initiated.")

    # 
    try:
        while True:
            print(f"Received data: {read_data()}")

    except KeyboardInterrupt or Exception:
        print("User interrupt or exception occured. Shutting down.")
        ser.close()

if __name__ == "__main__":
    main()
