import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(5)

print("Listening...")

while True:
    if ser.in_waiting:
        print(ser.readline().decode("utf-8", errors="ignore").strip())
