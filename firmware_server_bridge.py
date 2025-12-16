import platform
import serial
import time
import requests

WEBSERVER_URL = "http://127.0.0.1:8000"
CURRENT_PLATFORM = platform.system()

port_identifier = "COM5" if CURRENT_PLATFORM == "Windows" else "/dev/ttyACM0"
print(f"Running on a {CURRENT_PLATFORM} system, handshaking port '{port_identifier}'")
try:
    ser = serial.Serial(port_identifier, 9600, timeout=1)
except FileNotFoundError as e:
    print(f"Device unavailable at {e.filename}")
    exit();


print(f"Port ready, waiting for serial device on {port_identifier} to refresh")
time.sleep(5)
print(f"Listening and will transmit to server on {WEBSERVER_URL}")
while True:
    if ser.in_waiting:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        data = line.split(",")

        if len(data) < 2:
            print(data)
            continue

        payload = {
            "temperature": data[0],
            "humidity": data[1],
        }

        try:
            response = requests.post(WEBSERVER_URL, json=payload, timeout=2)
            print("Sent:", payload, "| Status:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("POST failed:", e)
