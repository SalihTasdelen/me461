import wifi
from socketpool import SocketPool
import os
from bugconfig import *
from bugeval import eval_args

def wifiConnect():
    print('Started Wifi Execution.')

    if not wifi.radio.connected:
        print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}.")
        wifi.radio.connect(
            os.getenv("CIRCUITPY_WIFI_SSID"), 
            os.getenv("CIRCUITPY_WIFI_PASSWORD")
        )

    print(f"Established Wifi connection to {os.getenv('CIRCUITPY_WIFI_SSID')}.")

    HOST = str(wifi.radio.ipv4_address)
    SERVER_ADDR = (HOST, SERVER_PORT)
    
    pool = SocketPool(wifi.radio)
    print('Created socket pool.')

    socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    socket.bind(SERVER_ADDR)

    socket.listen(1)
    print(f'Started execution server at {SERVER_ADDR}.')

    return socket

def serveClient(conn, addr):
    buff = bytearray(BUFFER_SIZE)
    waiting = True

    while waiting:
        numOfBytes, recvAddr = conn.recvfrom_into(buff)
        
        if numOfBytes:
            msg = buff[:numOfBytes].decode(FORMAT)
            print(f'Received: {msg}.')
            if msg == 'exit':
                waiting = False
                break
            results = eval_args([msg])
            for result in results:
                conn.sendto(bytearray(result, FORMAT), recvAddr)
        else:
            waiting = False

    conn.close()
    print(f'Connection is terminated {addr}.')


def wifiExecute():
    socket = wifiConnect()
    while True:
    # Blocking execution
        conn, addr = socket.accept()
        print(f'Connected by {addr}.')

        serveClient(conn, addr)