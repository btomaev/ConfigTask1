from fs import get_fs, ZipInfo, FS
from parser import parse_args
from datetime import datetime

CLI_NAME = "touch"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    help_str =  "Usage: touch [-c] [-d DATE] [-t DATE] [-r FILE] FILE..." +"\n\n" + \
                "Update the last-modified date on the given FILE[s]" +"\n\n" + \
                "    -h  --help     Show help message" +"\n" + \
                "    -c             Don't create files" +"\n"
    
    if "-h" in opts or "--help" in opts or len(pos) == 1:
        print(help_str)
        return
    
    dt = datetime.now().timetuple()

    for filename in pos[1:]:
        filename = pos[1] if pos[1].startswith("/") else fs.cwd + pos[1]
        if "-c" in opts or fs.is_file(filename):
            if fs.is_file(filename):
                with fs.open_file(filename, "r") as file:
                    content = file.read()
                    fileinfo = fs.get_info(filename)
                    fileinfo.date_time = dt
                fs.delete([filename])
                with fs.open_file(fileinfo, "w") as new_flie:
                    new_flie.write(content)
            else:
                print(f"{pos[1]} is not a file.")
        else:
            filename = FS._normalize_path(filename)
            mode = int("100644", base=8)
            fileinfo = ZipInfo(filename, dt)
            fileinfo.external_attr = ((0x1000000000 | mode) & 0xFFFF) << 16
            with fs.open_file(fileinfo, "w") as file:
                pass