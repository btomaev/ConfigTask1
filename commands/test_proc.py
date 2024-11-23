from time import sleep
from stdio import StdIO

CLI_NAME = "proc"

def run(cmd):
    print = lambda s: StdIO.stdout.write(s.encode())
    print("Hello from test command 1")
    sleep(1)
    print("Hello from test command 2")
    sleep(1)
    print("Hello from test command 3")
