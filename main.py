import os
import time
import subprocess

FAHRENHEIT = os.getenv("CONFIG_CELSIUS_OR_FAHRENHEIT", "F")
MIN_TEMP = int(os.getenv("CONFIG_MINIMUM_TEMPERATURE", 130))
MAX_TEMP = int(os.getenv("CONFIG_MAXIMUM_TEMPERATURE", 150))
MANUAL_MODE = os.getenv("CONFIG_MODO_MANUAL_DE_VELOCIDAD", "false") == "true"
MANUAL_SPEED = int(os.getenv("CONFIG_VELOCIDAD_MANUAL_DEL_VENTILADOR", 0))
LOG_TEMP = os.getenv("CONFIG_LOG_CURRENT_TEMPERATURE_EVERY_30_SECONDS", "true") == "true"

def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        raw = int(f.read().strip())
        temp_c = raw / 1000.0
        if FAHRENHEIT == "F":
            return round((temp_c * 9 / 5) + 32, 1)
        else:
            return round(temp_c, 1)

def calculate_fan_speed(temp):
    if temp <= MIN_TEMP:
        return 0
    elif temp >= MAX_TEMP:
        return 100
    else:
        return int(((temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)) * 100)

def set_fan_speed(speed_percent):
    speed_i2c = int(speed_percent * 255 / 100)
    subprocess.run(["i2cset", "-y", "1", "0x1a", "0x00", str(speed_i2c)], check=False)

while True:
    if MANUAL_MODE:
        speed = MANUAL_SPEED
    else:
        temp = get_temp()
        speed = calculate_fan_speed(temp)
        if LOG_TEMP:
            print(f"[{time.ctime()}] Temp: {temp}°, Fan Speed: {speed}%")

    set_fan_speed(speed)
    time.sleep(30)