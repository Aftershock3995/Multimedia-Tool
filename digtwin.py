import socket

HOST = "0.0.0.0"
PORT = 9000

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print("Waiting...")

while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("POS:", data.decode().strip())
