import socket

# Setup UDP Socket
UDP_IP = "0.0.0.0" 
UDP_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("UDP Listener Active. Waiting for Mach3...")

while True:
    data, addr = sock.recvfrom(1024) # Buffer size 1024 bytes
    print(f"Received from {addr}: {data.decode().strip()}")
