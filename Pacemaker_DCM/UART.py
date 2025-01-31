import serial 
import time
import user_processing
import struct
import serial.tools.list_ports
Sync = 16
FnCode = 11
receive = 22


def send_data(username,ser):
    """Send an 8-bit data byte over UART."""
    #Use little endian for UART com
    parameter_data = user_processing.getParameters(username)
    pacing = user_processing.getPacing(username)
    print(pacing)
    print(parameter_data)
    # {SYNC, FnCode, pacingState, pacingMode, hysteresis, hysteresisInterval, lowrateInterval, vPaceAmp, vPaceWidth, VRP}
    ser.write(struct.pack('<BBBBBBBhBBBhBBhBBBBB', Sync,FnCode,pacing,*parameter_data))

def receive_data(username,ser):
    """Receive an 8-bit data byte over UART."""
    parameter_data = user_processing.getParameters(username)
    pacing = user_processing.getPacing(username)
    data = ser.read(1)
    print(struct.unpack('<BBBBBBBhBBBhBBhBBBBB',data))

def get_serial_ports_info():
    devices = serial.tools.list_ports.comports()
    usb_devices = []
    
    for device in devices:
        usb_info = {
            "device": device.device,
            "serial_number": device.serial_number,
            "description": device.description,
            "manufacturer": device.manufacturer,
        }
        usb_devices.append(usb_info)
    try:
        return usb_devices[0]["serial_number"]
    except:
        return "no device"

    
    