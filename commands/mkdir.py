from fs import get_fs
from parser import parse_args

CLI_NAME = "mkdir"

def run(cmd):
    kwargs = {
        "--mode": 511
    }
    args, pos, opts, kwargs = parse_args(cmd, kwargs=kwargs)
    fs = get_fs()

    for dir_name in pos[1:]:
        fs.mkdir(("" if dir_name.startswith("/") else fs.cwd) + dir_name, mode=int(kwargs["--mode"]))