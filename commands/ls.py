from fs import get_fs
from parser import parse_args
from datetime import datetime
from stat import filemode

CLI_NAME = "ls"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    if len(pos) > 1:
        path = fs.cwd + pos[1] if pos[1].startswith("/") else pos[1]
    else:
        path = fs.cwd

    dir_content = fs.list_dir(path)

    if dir_content:
        max_name_len = max([len(path.at) for path, _ in dir_content])
        if "-l" in opts:
            print(f"{"mode":<10}  {"name":<{max_name_len}}  {"modified":>19}  {"size":>10}")
            for path, file in dir_content:
                hi = file.external_attr >> 16
                print(hi)
                print(f"{filemode(hi):<10}  {path.name + "/" if path.is_dir() else path.name:<{max_name_len}}  {datetime(*file.date_time).strftime("%d/%m/%Y %H:%M:%S"):>19}  {file.file_size:>10}")
        else:
            for path, file in dir_content:
                print(path.name + "/" if path.is_dir() else path.name, end="  ")
            print()
    