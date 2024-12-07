import pkgutil, sys
from importlib.util import module_from_spec

_all_commands = {}
_initialized = False

class CommandLoadError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

class CommandNotFoundError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

def check_object_exists(m, obj):
    return obj in m.__dict__

def check_function_exists_and_callable(m, func):
    return check_object_exists(m, func) and callable(m.__dict__[func])

def get_commands():
    global _initialized, _all_commands
    if _initialized:
        return _all_commands
    package = sys.modules[__name__]
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        try:
            fullname = "commands.%s" % modname
            if fullname in sys.modules:
                m = sys.modules[fullname]
            else:
                spec = importer.find_spec(fullname)
                m = module_from_spec(spec)
                spec.loader.exec_module(m)
        except:
            raise CommandLoadError(f"Failed to load command '{modname.lower()}'")
        if not check_function_exists_and_callable(m, "run") and check_object_exists(m, "CLI_NAME"):
            continue
        _all_commands[m.CLI_NAME.lower()] = m
    _initialized = True
    return _all_commands