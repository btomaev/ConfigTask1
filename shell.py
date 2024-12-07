from argparse import ArgumentParser
from fs import mount
from commands import get_commands
from logs import get_logger
from system import login
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys, os

def main():
    parser = ArgumentParser()
    parser.add_argument('fs', help='path to fs zip-archive')
    parser.add_argument('--user', help='current user name', default="root")
    parser.add_argument('--log', help='path to log file (csv)', default="logs/log.csv")
    parser.add_argument('--startup', help='path to startup script', default=None)
    parser.add_argument('--hostname', help='current hostname', default="fakenix")
    parser.add_argument('--here', action="store_true")

    args = parser.parse_args()

    fs = mount(args.fs)
    try:
        fs.is_dir("/")
    except Exception as e:
        print(f"FS error: {e}")
        exit(1)

    if not args.here:
        Popen(" ".join(["python"] + sys.argv + ["--here"]), creationflags=CREATE_NEW_CONSOLE)
        return
    
    os.makedirs(os.path.dirname(args.log), exist_ok=True)

    sys_info = login(args.user, args.hostname)
    user = f"{sys_info.username}@{sys_info.hostname}"
    logger = get_logger(args.log, user)
    commands = get_commands()
    
    if args.startup:
        with open(args.startup, "r") as file:
            for command in file.readlines():
                args = command.split()
                cmd = commands.get(args[0])
                logger.info(cmd_str)
                if not cmd:
                    continue
                cmd.run(cmd_str)

    while True:
        cmd_str = input(f"{user} {fs.cwd}# ").strip()
        args = cmd_str.split()
        cmd = commands.get(args[0])

        logger.info(cmd_str)
        
        if not cmd:
            print(f"Command {args[0]} not found.")
            continue

        cmd.run(cmd_str)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass