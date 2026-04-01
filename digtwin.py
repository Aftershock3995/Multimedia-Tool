import socket

# Must match the IP and Port in your VB Script
HOST = '192.168.10.2'
PORT = 502 

def start_server():
    # Create a standard TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Direct Listener Active on {HOST}:{PORT}")
        print("Waiting for Mach3 VB Script...")

        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    # Receive the raw string: "X,Y,Z"
                    data = conn.recv(1024).decode('utf-8')
                    if data:
                        # Split the string by the comma
                        coords = data.split(',')
                        
                        # Ensure we got all three axes
                        if len(coords) == 3:
                            x, y, z = coords
                            print(f"X: {x:>7} | Y: {y:>7} | Z: {z:>7}", end="\r")
                except Exception as e:
                    # If the data is garbled, just skip it
                    pass

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nListener Stopped.")
