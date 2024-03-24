from . import serialsocks

from functools import partial

import pickle

make_server = partial(serialsocks.make_server, pickle)
send = partial(serialsocks.send, pickle)