SERVER_PORT = 5050
BUFFER_SIZE = 512
FORMAT = 'utf-8'
TERMINATOR = '\n'

import supervisor

if supervisor.runtime.autoreload:
    supervisor.runtime.autoreload = False