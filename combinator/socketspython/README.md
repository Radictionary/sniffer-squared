# pickledsocks


Facilitate connections processes.

Python programs communicate amongst themselves with `pickle` or `json`.
They must communicate with non-python programs with `json`, because
of course non-python processes cannot use `pickle`.


Here's the code, an overview of the important functions:

```python
class picklesocks:
    python_make_server = partial(make_server, pickle)
    python_send = partial(send, pickle)

class jsoncks:
    make_server = partial(make_server, json)
    send = partial(send, json)
```

# Simple test program:

```python

import sys

from pickledsocks import jsoncks

is_server = sys.argv[1].strip() == 'y'

def get(data):
    print(f"I got data: {data}")
    return "I got your dataif is_server:

if is_server:
    asyncio.run(jsoncks.make_server(get, 3952))
else:
    asyncio.run(jsoncks.send("Hi server from client!", 3952))
```