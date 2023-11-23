import time
from bugwifi import wifiExecute
from bugserial import serialExecute



while True:
    option = input('Select a server option (wifi/serial): ')

    if option == 'wifi':
        wifiExecute()
    elif option == 'serial':
        serialExecute()
    else:
        print('Unrecognized option.')
        break





