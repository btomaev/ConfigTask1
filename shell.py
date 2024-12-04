from argparse import ArgumentParser
from fs import mount
from commands import get_commands
from logs import get_logger
from system import login

def main():
    parser = ArgumentParser()
    parser.add_argument('fs', help='path to fs zip-archive')
    parser.add_argument('--user', help='current user name', default="root")
    parser.add_argument('--log', help='path to log file (csv)', default="log.csv")
    parser.add_argument('--startup', help='path to startup script', default=None)
    parser.add_argument('--hostname', help='current hostname', default="fakenix")

    args = parser.parse_args()

    sys_info = login(args.user, args.hostname)
    user = f"{sys_info.username}@{sys_info.hostname}"
    logger = get_logger("log.csv", user)
    commands = get_commands()
    fs = mount("fs.zip")

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