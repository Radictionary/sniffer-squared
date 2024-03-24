
from . import serialsocks

import json
from functools import partial, wraps

def bytesify_output(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return bytes(f(*args, **kwargs), encoding="utf-8")
    return wrapper

def stringify_input(f):
    @wraps(f)
    def wrapper(input_, *args, **kwargs):
        return f(str(input_, encoding="utf-8"), *args, **kwargs)
    return wrapper

# modify the json functions so that they work with bytes.
# for some reason pickle & json are incompatible 
# because pickle.loads takes bytes & json.loads takes str
# (same for outputs of X.dumps)

new_json_dumps = bytesify_output(json.dumps)
new_json_loads = stringify_input(json.loads)

make_server = partial(serialsocks.make_server, new_json_dumps, new_json_loads)
send = partial(serialsocks.send, new_json_dumps, new_json_loads)
