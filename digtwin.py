from ftplib import FTP
import time

# --- CONFIGURATION ---
WINDOWS_IP = "192.168.10.x"  # Change to your Mach3 PC IP
WIN_USER = "chres"          # Your Windows Username
WIN_PASS = "00003766"    # Your Windows Password

def get_mach3_data():
    try:
        # Connect and Login
        ftp = FTP(WINDOWS_IP)
        ftp.login(user=WIN_USER, passwd=WIN_PASS)
        
        # Download the file content into a list
        lines = []
        ftp.retrlines('RETR coords.txt', lines.append)
        
        ftp.quit() # Close connection cleanly
        
        if lines:
            return lines[0].strip()
    except Exception as e:
        # This will tell you if it's "Login Denied" or "Connection Refused"
        print(f"Error: {e}")
        return None

print(f"Attempting to connect to {WINDOWS_IP}...")

while True:
    data = get_mach3_data()
    if data:
        try:
            # Splits the "10.5, 5.0, 0.0" into separate variables
            x, y, z = data.split(",")
            print(f"LIVE DRO -> X: {x} | Y: {y} | Z: {z}")
        except ValueError:
            print("File exists but format is wrong. Check Mach3 script.")
    else:
        print("Retrying connection...")
    
    time.sleep(0.1) # 10 times per second
