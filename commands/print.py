from fs import get_fs
from parser import parse_args

CLI_NAME = "print"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    if len(pos) > 1:
        filename = pos[1] if pos[1].startswith("/") else fs.cwd + pos[1]
        if not fs.is_file(filename):
            print(f"{pos[1]} is not a file.")
            return
        with fs.open_file(filename, mode="r") as file:
            print(file.read().decode())
            