import serial

ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    data = ser.readline().decode().strip()
    print(data)
