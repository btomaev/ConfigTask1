from threading import Thread

from fs import mount
from commands import get_commands
from system import login
from stdio import StdIO



def main():
    commands = get_commands()
    fs = mount("fs.zip")
    sys_info = login("fox", "foxhole")

    while True:
        cmd_str = input(f"{sys_info.username}@{sys_info.hostname} {fs.cwd}# ").strip()
        args = cmd_str.split()
        cmd = commands.get(args[0])
        
        if not cmd:
            print(f"Command {args[0]} not found.")
            continue

        cmd.run(cmd_str)
        
        # try:
        # proc = Thread(target=cmd.run, args=(cmd_str,))
        # proc.start()

        # while proc.is_alive():
        #     pass
        #     if out := StdIO.stdout.readline():
        #         print(out)

        # if status:
        #     print(f"Command {args[0]} exited with status {status}")
        #     continue

        # except:
        #     pass