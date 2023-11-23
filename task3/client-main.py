#!/usr/bin/env python3
import argparse

FORMAT = 'utf-8'

parser = argparse.ArgumentParser()
parser.add_argument('-p', "--port", type=str, help="Serial/Socket port of the board", nargs=1)
parser.add_argument("--host", type=str, help="IP address of the board", nargs='?')
parser.add_argument('-e', "--evalList", type=str, help="Arguments to be evaluated.", nargs='+')


def evalWifi(host, port, evalList):
    import socket
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(None)

        print(f'Connecting to ({host}, {port}).')
        s.connect((host, port))

        for evalElem in evalList:
            s.send(bytearray(evalElem, FORMAT))
            data = s.recv(1024)
            print(data.decode())        


def evalSerial(port, evalList):
    import serial

    channel = serial.Serial(port)
    channel.timeout = 0.05

    for evalElem in evalList:
        channel.write(bytearray(evalElem + '\n', FORMAT))
        output = channel.readline()    
        print(output.decode())


if __name__ == '__main__':
    args = parser.parse_args()
    port = args.port
    host = args.host
    evalList = args.evalList
    
    print(".......................hi....")

    if host:
        evalWifi(host, int(port[0]), evalList)    
    else:
        evalSerial(port[0], evalList)
    print(".......................bye...")