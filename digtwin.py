import urllib.request
import time

URL = "http://192.168.10.1:8000/coords.txt"

def get_coords():
    try:
        with urllib.request.urlopen(URL, timeout=1) as response:
            data = response.read().decode().strip()
            if data:
                return data.split(",")
    except:
        return None

print("Reading Mach3 over HTTP...")

while True:
    coords = get_coords()
    
    if coords and len(coords) == 3:
        print(f"X: {coords[0]} | Y: {coords[1]} | Z: {coords[2]}")
    else:
        print("Waiting...")
    
    time.sleep(0.1)
