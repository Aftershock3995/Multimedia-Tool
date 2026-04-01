import socket
import struct

# Network Settings
HOST = '192.168.10.2'
PORT = 502

# Data Store
registers = {0: 0.0, 1: 0.0, 2: 0.0}

def process_data(data):
    """Processes the Modbus buffer and updates registers."""
    ptr = 0
    responses = b""
    
    # Debug: Print raw hex to see what Mach3 is actually sending
    # If this shows all zeros (0000...), Mach3 isn't sending real data yet
    raw_hex = data.hex()
    
    # Each Modbus TCP 'Write Single Register' (Func 6) packet is 12 bytes
    while ptr + 12 <= len(data):
        packet = data[ptr:ptr+12]
        func_code = packet[7]
        
        if func_code == 6:
            # Extract Address and Value
            reg_addr = struct.unpack('>H', packet[8:10])[0]
            raw_val = struct.unpack('>H', packet[10:12])[0]
            
            # Handle Negative Numbers (Two's Complement)
            signed_val = raw_val if raw_val <= 32767 else raw_val - 65536
            
            # Update our internal dictionary
            registers[reg_addr] = signed_val / 100.0
            
            # Modbus TCP requires echoing the packet back as confirmation
            responses += packet
            
        ptr += 12 
    return responses, raw_hex

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
        except PermissionError:
            print("Error: Permission Denied. Use 'sudo'.")
            return
            
        s.listen(1)
        print(f"Server Active on {HOST}:{PORT}")
        print("Waiting for Mach3...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\nConnected by Mach3 at {addr}")
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data: break
                        
                        reply, raw = process_data(data)
                        if reply:
                            conn.sendall(reply)
                        
                        # Display output
                        out = f"X: {registers.get(0,0):.2f} | Y: {registers.get(1,0):.2f} | Z: {registers.get(2,0):.2f}"
                        # Check if data is actually arriving or if it's just empty pings
                        if "0600" in raw: # Function code 6 + address 00
                            print(f"{out} [DATA OK]", end="\r")
                        else:
                            print(f"{out} [NO DATA IN PACKET]", end="\r")
                            
                    except ConnectionResetError:
                        break
                print("\nMach3 Disconnected. Waiting for reconnect...")

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer Stopped.")
