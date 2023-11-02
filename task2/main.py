from pong.game.server import PongServer
from pong.mpi.pipe import BindingPipe, ConnectingPipe
from pong.game.client import PongClient
from pong.mpi import *
import logging

# Logging
level = logging.WARNING
logging.basicConfig(format='%(levelname)s: %(message)s', level=level)

def main():
    role = input("Enter 'server' or 'client': ").strip().lower()
    if role == 'server':
        server = BindingPipe(maxConnection=2, timeOut=None)
        pongServer = PongServer(server)
        pongServer.gameLoop()
    elif role == 'client':
        client = ConnectingPipe()
        pongClient = PongClient(client, SERVER_ADDR, maxDx=100, maxLagTime=100e-3)
        pongClient.gameLoop()
        pongClient.quit()
    else:
        logging.error("[MAIN] Invalid input. Please enter 'server' or 'client'.")

if __name__ == "__main__":
    main()
