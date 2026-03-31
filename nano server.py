import socket
import time

HOST = "0.0.0.0"
PORT = 9000

while True:
    try:
        print("Waiting for Mach3...")
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        conn, addr = s.accept()
        print("Connected:", addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()
            print(msg)

    except Exception as e:
        print("Error:", e)

    finally:
        try:
            conn.close()
        except:
            pass
        s.close()

    print("Reconnecting in 2 sec...")
    time.sleep(2)