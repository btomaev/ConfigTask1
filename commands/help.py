from commands import get_commands

CLI_NAME = "help"

def run(cmd):
    commands = get_commands()
    print("  ".join(commands))
    