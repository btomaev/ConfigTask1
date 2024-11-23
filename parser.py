from typing import List, Dict, Any

def split_args(arg_string: str):
    p = 0
    quote_flag = False
    word = ""
    args: List[str] = []

    while p < len(arg_string) or word:
        if p >= len(arg_string) or arg_string[p] == " " and not quote_flag:
            if word:
                args.append(word)
            word = ""
            p += 1
            continue
        elif arg_string[p:p+2] == "\\\"":
            p += 1
            continue
        elif arg_string[p] == "\"":
            quote_flag = not quote_flag
            p += 1
            continue
        
        word += arg_string[p]

        p += 1
        
    return args

def parse_args(arg_string: str, kwargs: Dict[str, Any]={}):
    p = 0
    options = set()
    positional: List[str] = []

    args = split_args(arg_string)

    while p < len(args):
        if args[p].startswith("--"):
            if "=" in args[p]:
                key, value = args[p].split("=")
            else:
                key = args[p]
                value = args[p+1] if p+1 < len(args) else None
            if key in kwargs:
                if value:
                    kwargs.update({key: value})
                    p += 2
                    continue
            else:
                options.add(args[p])
        elif args[p].startswith("-"):
            opts = args[p][1:]
            options.update(map(lambda o: f"-{o}", opts))
        else:
            positional.append(args[p])

        p += 1
        
    return args, positional, options, kwargs