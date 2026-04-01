from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import threading
import time

# Create 100 registers. 
# Mach3 will write to address 0, 1, and 2.
store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)

def display_logic():
    while True:
        # Read the first 3 registers (X, Y, Z)
        raw_data = store.getValues(3, 0, 3)
        
        # Convert back from "Integer * 100" to Float
        # This handles the decimal places we sent from Mach3
        processed = [round(val / 100.0, 2) for val in raw_data]
        
        print(f"MACH3 DATA -> X: {processed[0]} | Y: {processed[1]} | Z: {processed[2]}      ", end="\r")
        time.sleep(0.1)

# Run display in background
threading.Thread(target=display_logic, daemon=True).start()

print("Pi Modbus Server Active on 192.168.10.2:502")
StartTcpServer(context=context, address=("192.168.10.2", 502))
