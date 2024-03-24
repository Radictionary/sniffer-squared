from . import serialsocks

from functools import partial

import pickle

make_server = partial(serialsocks.make_server, pickle.dumps, pickle.loads)
send = partial(serialsocks.send, pickle.dumps, pickle.loads)