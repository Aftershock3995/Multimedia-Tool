from ftplib import FTP
import time

# --- CONFIG ---
WINDOWS_IP = "192.168.10.1" # Your Mach3 PC IP

def get_mach3_data():
    try:
        ftp = FTP(WINDOWS_IP)
        ftp.login() # Anonymous login
        
        # Download the file into a list
        lines = []
        ftp.retrlines('RETR coords.txt', lines.append)
        ftp.quit()
        
        if lines:
            return lines[0].strip()
    except Exception as e:
        return None

print("Link Established. Monitoring Mach3...")

while True:
    data = get_mach3_data()
    if data:
        try:
            x, y, z = data.split(",")
            print(f"X: {x} | Y: {y} | Z: {z}")
        except:
            pass
    else:
        print("Searching for file...")
    
    time.sleep(0.1) # 10Hz Refresh
