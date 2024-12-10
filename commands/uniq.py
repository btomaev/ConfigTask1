from parser import parse_args
from fs import get_fs

CLI_NAME = "uniq"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    help_str =  "Usage: uniq [-hdui] [INPUT]" +"\n\n" + \
                "Discard duplicate lines" +"\n\n" + \
                "    -h  --help     Show help message" +"\n" + \
                "    -d             Only print duplicate lines" +"\n" + \
                "    -u             Only print unique lines" +"\n" + \
                "    -i             Ignore case\n"
    
    if "-h" in opts or "--help" in opts or len(pos) == 1:
        print(help_str)
        return
    
    path = pos[1] if pos[1].startswith("/") else fs.cwd + pos[1]
    if not fs.is_file(path):
        print(f"{pos[1]} is not a file.")
        return
    with fs.open_file(path) as file:
        dup_flag = False
        uniq = not "-d" in opts
        ignore_case = "-i" in opts
        curr = file.readline().rstrip(b"\r\n").decode()
        while curr:
            prev = curr
            curr = file.readline().rstrip(b"\r\n").decode()

            if prev.lower() == curr.lower() if ignore_case else prev == curr:
                if not (uniq or dup_flag):
                    print(curr)
                dup_flag = True
            else:
                if uniq:
                    print(prev)
                dup_flag = False