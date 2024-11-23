from fs import get_fs
from parser import parse_args

CLI_NAME = "touch"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    help_str =  "Usage: touch [-c] [-d DATE] [-t DATE] [-r FILE] FILE..." +"\n\n" + \
                "Update the last-modified date on the given FILE[s]" +"\n\n" + \
                "    -h  --help     Show help message" +"\n" + \
                "    -c             Don't create files" +"\n" + \
                "    --ref FILE     Use FILE's date/time"
    
    if "-h" in opts or "--help" in opts or len(pos) == 1:
        print(help_str)
        return

    for filename in pos[1:]:
        filename = pos[1] if pos[1].startswith("/") else fs.cwd + pos[1]
        if "-c" in opts:
            if fs.is_file(filename):
                with fs.open_file(filename, "w") as new_flie:
                    with fs.open_file(filename, "r") as file:
                        new_flie.write(file.read())
            else:
                print(f"{pos[1]} is not a file.")
        else:
            file = fs.open_file(filename, "w")
            file.close()