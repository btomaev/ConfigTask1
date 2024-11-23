from fs import get_fs
from parser import parse_args

CLI_NAME = "cd"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    if len(pos) > 1:
        if not fs.cd(("" if pos[1].startswith("/") else fs.cwd) + pos[1]):
            print(f"{pos[1]} is not a directory.")