from platform import processor, architecture, machine

from system import get_sys_info
from parser import parse_args
from fs import get_fs

CLI_NAME = "uname"

def run(cmd):
    args, pos, opts, kwargs = parse_args(cmd)
    fs = get_fs()

    help_str =  "Usage: uname [-hamnpio]" + "\n\n" + \
                "Print system information" + "\n\n" + \
                "    -h  --help     Print help" + "\n" + \
                "    -a             Print all" + "\n" + \
                "    -m             The machine (hardware) type" + "\n" + \
                "    -n             Hostname" + "\n" + \
                "    -p             Processor type" + "\n" + \
                "    -i             The hardware platform" + "\n" + \
                "    -o             OS name"
    
    if "-h" in opts or "--help" in opts:
        print(help_str)
        return
    
    sys_info = get_sys_info()
    
    specs = {
        "os": sys_info.os_name,
        "hostname": sys_info.hostname,
        "platform": "_".join(architecture()),
        "hw": machine(),
        "processor": processor(),
    }
    
    output = ""

    if not opts:
        opts.update(("-o", "-n"))

    if "-a" in opts:
       opts.update(("-no", "-n", "-i", "-m", "-p"))

    if "-o" in opts:
        output += f"OS: {specs["os"]}\n"
    if "-n" in opts:
        output += f"Hostname: {specs["hostname"]}\n"
    if "-i" in opts:
        output += f"Platform: {specs["platform"]}\n"
    if "-m" in opts:
        output += f"Architecture: {specs["hw"]}\n"
    if "-p" in opts:
        output += f"Processor: {specs["processor"]}\n"

    print(output)
    