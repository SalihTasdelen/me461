## Connect to Wifi Server
    python main.py --port 5050 --host "192.168.1.108" -e '29/342' 'sin(41)' 'sqrt(89)'

## Connect to Serial Server
    python main.py --port /dev/ttyACM1 -e '29/342' 'sin(41)' 'sqrt(89)'

## Start Wifi or Serial Server on RP Pico W
    screen /dev/ttyACM0 115200
    choose serial or wifi

