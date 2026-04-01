import urllib.request
import time

# --- CONFIG ---
# Replace with your Windows IP and the folder share name
# Format: http://[IP]/[ShareName]/coords.txt
url = "http://192.168.10.5/Mach3Mill/coords.txt" 

def get_data():
    try:
        # Pulls the file directly from the Windows network share
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8').strip()
    except Exception as e:
        return None

print("Listening for Mach3 Motion...")

while True:
    raw_data = get_data()
    if raw_data:
        try:
            x, y, z = raw_data.split(",")
            print(f"ABS POS -> X: {x} | Y: {y} | Z: {z}")
        except:
            pass # Handle partial file writes
    else:
        print("Searching for Mach3 on network...")
    
    time.sleep(0.05) # 20Hz update rate
