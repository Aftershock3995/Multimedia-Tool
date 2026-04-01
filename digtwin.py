import subprocess
import time

# --- CONFIG ---
WIN_USER = "chres"          # Your Windows Username
WIN_IP = "192.168.10.1"      # Your Windows IP
FILE_PATH = "C:/Mach3/macros/Mach3Mill/coords.txt"

def get_remote_coords():
    try:
        # This tells the Pi to run an SSH command to 'cat' (read) the file
        cmd = ["ssh", f"{WIN_USER}@{WIN_IP}", f"type {FILE_PATH}"]
        
        # Run the command and capture the output
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        data = result.decode('utf-8').strip()
        
        if data:
            return data.split(",")
    except Exception as e:
        return None

print(f"Connecting to Mach3 via SSH at {WIN_IP}...")

while True:
    coords = get_remote_coords()
    if coords and len(coords) == 3:
        print(f"X: {coords[0]} | Y: {coords[1]} | Z: {coords[2]}")
    else:
        print("Waiting for data or SSH Key...")
    
    time.sleep(0.1)
