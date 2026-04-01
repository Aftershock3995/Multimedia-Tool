import socket
import struct

# =========================
# CONFIG
# =========================
HOST = '192.168.10.2'   # Pi IP
PORT = 502              # Modbus TCP port

# Store register values
registers = {}

# =========================
# MODBUS PROCESSOR
# =========================
def process_data(data):
    responses = b""
    raw_hex = data.hex()

    print(f"\nRAW RX: {raw_hex}")

    if len(data) < 8:
        return responses, raw_hex

    func_code = data[7]

    # =========================
    # FUNCTION 6 (WRITE SINGLE REGISTER)
    # =========================
    if func_code == 6 and len(data) >= 12:
        reg_addr = struct.unpack('>H', data[8:10])[0]
        raw_val = struct.unpack('>H', data[10:12])[0]

        # Convert to signed
        signed_val = raw_val if raw_val <= 32767 else raw_val - 65536

        registers[reg_addr] = signed_val / 100.0

        print(f"[FC6] Addr: {reg_addr} | Value: {registers[reg_addr]}")

        # Echo packet back (required)
        responses = data

    # =========================
    # FUNCTION 16 (WRITE MULTIPLE REGISTERS)
    # =========================
    elif func_code == 16:
        start_addr = struct.unpack('>H', data[8:10])[0]
        num_regs = struct.unpack('>H', data[10:12])[0]
        byte_count = data[12]

        print(f"[FC16] Start: {start_addr} | Count: {num_regs}")

        for i in range(num_regs):
            val = struct.unpack('>H', data[13 + i*2:15 + i*2])[0]
            signed_val = val if val <= 32767 else val - 65536

            registers[start_addr + i] = signed_val / 100.0

            print(f"  -> Reg {start_addr + i}: {registers[start_addr + i]}")

        # Response = transaction header + func + addr + count
        responses = data[:12]

    else:
        print(f"[UNKNOWN FUNC] Code: {func_code}")

    return responses, raw_hex


# =========================
# SERVER LOOP
# =========================
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((HOST, PORT))
        except PermissionError:
            print("❌ Permission denied. Run with sudo.")
            return

        s.listen(1)

        print(f"✅ Modbus Server running on {HOST}:{PORT}")
        print("⏳ Waiting for Mach3...\n")

        while True:
            conn, addr = s.accept()
            print(f"🔌 Connected by Mach3: {addr}")

            with conn:
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break

                        reply, raw = process_data(data)

                        if reply:
                            conn.sendall(reply)

                        # Display X Y Z (Regs 0,1,2)
                        x = registers.get(0, 0.0)
                        y = registers.get(1, 0.0)
                        z = registers.get(2, 0.0)

                        print(f"📍 X: {x:.2f} | Y: {y:.2f} | Z: {z:.2f}")

                    except ConnectionResetError:
                        break

            print("⚠️ Mach3 Disconnected. Waiting...\n")


# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
