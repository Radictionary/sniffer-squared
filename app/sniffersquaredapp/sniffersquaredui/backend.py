from functools import partial

RUN_FILE_PATH = "../../packet_pool/run.txt"

def write_to_runfile(data):
    with open(RUN_FILE_PATH) as f:
        f.write(data)

shutdown = partial(write_to_runfile, "false")
start    = partial(write_to_runfile, "true")