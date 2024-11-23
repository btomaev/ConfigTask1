from fs import get_fs

CLI_NAME = "pwd"

def run(cmd):
    fs = get_fs()
    print(fs.cwd)