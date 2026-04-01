import socket
import struct

# Network Settings
HOST = '192.168.10.2'  # The Pi's Static IP
PORT = 502             # Standard Modbus Port

# This dictionary acts as our "Holding Registers"
# Address 0, 1, 2 for X, Y, Z
registers = {0: 0, 1: 0, 2: 0}

def handle_modbus_packet(data):
    # Modbus TCP Header is 7 bytes
    # [Transaction ID(2)][Protocol ID(2)][Length(2)][Unit ID(1)]
    if len(data) < 7: return None
    
    unit_id = data[6]
    function_code = data[7]
    
    # Function Code 6 = Write Single Register (What Mach3 uses for Output-Holding)
    if function_code == 6:
        register_addr = struct.unpack('>H', data[8:10])[0]
        value = struct.unpack('>H', data[10:12])[0]
        
        # Handle Signed Integers (Two's Complement)
        if value > 32767:
            signed_val = value - 65536
        else:
            signed_val = value
            
        registers[register_addr] = signed_val / 100.0
        return data[0:12] # Echo back the request (Modbus standard)
    
    return None

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server Listening on {HOST}:{PORT} (No Packages Needed)")
        
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    
                    response = handle_modbus_packet(data)
                    if response:
                        conn.sendall(response)
                        
                    # Print the current status
                    print(f"X: {registers.get(0, 0):.2f} | Y: {registers.get(1, 0):.2f} | Z: {registers.get(2, 0):.2f}", end="\r")

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer Stopped.")
