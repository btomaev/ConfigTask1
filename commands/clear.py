from os import system

CLI_NAME = "clear"

def run(cmd):
    # print("\x1b[2J\x1b[H")
    system("cls||clear")