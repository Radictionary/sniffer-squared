# pickledsocks


Facilitate connections processes.

Python programs communicate amongst themselves with `pickle` or `json`.
They must communicate with non-python programs with `json`, because
of course non-python processes cannot use `pickle`.


Here's the code, an overview of the important functions:

```python
python_make_server = partial(make_server, pickle)
python_send = partial(send, pickle)


json_make_server = partial(make_server, json)
json_send = partial(send, json)
```

# Simple test program:

```python

import sys
import pickledsocks

is_server = sys.argv[1].strip() == 'y'

def get(data):
    print(f"I got data: {data}")
    return "I got your dataif is_server:

if is_server:
    asyncio.run(module.json_make_server(get, 3952))
else:
    asyncio.run(module.json_send("Hi server from client!", 3952))
```