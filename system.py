from dataclasses import dataclass

@dataclass
class SysInfo:
    username: str
    hostname: str
    os_name: str = "FakeNIX"

def login(username, hostname):
    global SYS_INFO
    SYS_INFO = SysInfo(
        username=username,
        hostname=hostname
    )
    return SYS_INFO

def get_sys_info():
    global SYS_INFO
    return SYS_INFO