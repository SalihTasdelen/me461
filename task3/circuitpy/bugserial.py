import usb_cdc
from bugconfig import *
from bugeval import eval_args


def serialConnect():
    print('Started Serial Execution.')

    serial = usb_cdc.data
    
    print(f'Established Serial connection.')
    serial.reset_input_buffer()

    return serial

def serveClient(serial):
    buff = bytearray(BUFFER_SIZE)

    while serial.connected:
        
        if serial.in_waiting:
            msg = serial.readline()
            print(f'Received: {msg}.')
            results = eval_args([msg[:-1].decode()])
            for result in results:
                serial.write(result.encode())


def serialExecute():
    
    serial = serialConnect()
    
    while True:
        serveClient(serial)